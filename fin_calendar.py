import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm
import numpy as np
from streamlit_autorefresh import st_autorefresh
from streamlit_js_eval import streamlit_js_eval

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

def unique(list):
    x = np.array(list)
    return np.unique(x)

def dispaly_calendar():
    if st.button("캘린더가 보이지 않을 시 클릭"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")


    def create_month_year_events(data, salaries):
        # Extract Year-Month and Year for grouping
        data['month_year'] = data['지출일'].dt.to_period('M')
        data['year'] = data['지출일'].dt.to_period('Y')
        
        # Aggregate data for month and year
        monthly_data = data.groupby('month_year').agg({'지출금액': 'sum'}).reset_index()
        yearly_data = data.groupby('year').agg({'지출금액': 'sum'}).reset_index()
        
        # Create monthly and yearly salary data
        monthly_salaries = {pd.to_datetime(date): amount for date, amount in salaries.items()}
        yearly_salaries = {
            pd.to_datetime(f"{year}-01-01"): sum(amount for date, amount in salaries.items() if date.startswith(str(year)))
            for year in set(date.split("-")[0] for date in salaries)
        }

    def calculate_monthly_totals(data):
    # Resample data to monthly frequency, summing amounts
        monthly_totals = data.resample('M', on='지출일').sum()
        return monthly_totals

    def calculate_yearly_totals(data):
        # Resample data to yearly frequency, summing amounts
        yearly_totals = data.resample('Y', on='지출일').sum()
        return yearly_totals

    def display_monthly_totals(monthly_totals):
        st.subheader("Monthly Totals")
        st.line_chart(monthly_totals['지출금액'])

    def display_yearly_totals(yearly_totals):
        st.subheader("Yearly Totals")
        #st.dataframe(yearly_totals)
        st.line_chart(yearly_totals['지출금액'])


    def load_data():
        data = pd.read_excel("통합 문서1.xlsx")
        
        data['지출일'] = pd.to_datetime(data['지출일'], format='%Y.%m.%d')
        original_start_date = data['지출일'].min()
        original_end_date = data['지출일'].max()
        new_end_date = pd.to_datetime("2024-08-06")
        date_difference = new_end_date - original_end_date

        data['지출일'] = data['지출일'] + date_difference

        data['지출금액'] = pd.to_numeric(data['지출금액'], errors='coerce')
        data['지출금액'] = data['지출금액'].fillna(method='ffill')
        data['지출금액'] = data['지출금액'].astype(int)
        
        daily_expenditure = data.groupby('지출일')['지출금액'].sum().reset_index()
        print(daily_expenditure.info())
        return data, daily_expenditure

    def create_events(daily_expenditure, salaries):
        # Current date
        now = pd.to_datetime("today")
        
        # One month ago from the current date
        one_month_ago = now - pd.DateOffset(months=1)
        
        events = [
            {
                "start": str(date),
                "end": str(date),
                "title": f"{amount}원",
                "color": "blue" if date > one_month_ago else "grey"  # Change color based on the date
            } 
            for date, amount in zip(daily_expenditure['지출일'], daily_expenditure['지출금액'])
        ]
        
        # Adding salary events
        for date, salary in salaries.items():
            events.append({
                "start": str(date),
                "end": str(date),
                "title": f"{salary}원",
                "color": "green" if pd.to_datetime(date) > one_month_ago else "grey"
            })
        
        return events
    
    def display_pie_chart(data, viewing_year, viewing_month, viewing_day):
        fontRegistered()
        #fontNames = [f.name for f in fm.fontManager.ttflist]
        fontname = 'NanumGothic'

        plt.rc('font', family=fontname)

        daily_data = data[
            (data['지출일'].dt.day == viewing_day) &
            (data['지출일'].dt.month == viewing_month) & 
            (data['지출일'].dt.year == viewing_year)
        ]

        # Group by category and sum the expenditure
        category_totals = daily_data.groupby('카테고리')['지출금액'].sum()

        # Create a pie plot
        fig, ax = plt.subplots()
        
        ax.pie(category_totals, labels = category_totals.index, autopct='%1.1f%%', startangle=90)
        ax.legend(category_totals.index, title="Categories", loc="best")

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Add a title
        plt.title(f'Expenditure by Category on {viewing_year}-{viewing_month}-{viewing_day}')

        # Show the plot in Streamlit
        st.pyplot(fig)



    def display_details(details, selected_date_str, selected_date, salaries):
        # Expenditure for the selected date
        expenditure = details['지출금액'].sum()
        
        # Income till the selected date
        total_income = sum(v for k, v in salaries.items() if k <= selected_date_str)
        
        # Expenditure till the selected date
        total_expenditure = details[details['지출일'] <= pd.Timestamp(selected_date)]['지출금액'].sum()
        
        # Calculate total assets till the selected date: total income - total expenditure
        total_assets = total_income - total_expenditure
        
        st.subheader(f"Details for {selected_date}")
        st.dataframe(details)
        
        st.markdown(f"**Income on {selected_date}:** {salaries.get(selected_date_str, 0)}원")
        st.markdown(f"**Expenditure on {selected_date}:** {expenditure}원")
        st.markdown(f"**Total Assets till {selected_date}:** {total_assets}원")


    def display_graph(data):
        col1, col2 = st.columns(2)
        
        monthly_totals = calculate_monthly_totals(data)
        yearly_totals = calculate_yearly_totals(data)
        with col1:
            display_monthly_totals(monthly_totals)

        with col2:
            display_yearly_totals(yearly_totals)

        
    def fin_calendar():
        #st_autorefresh(interval=10000, key="hello")
        data, daily_expenditure = load_data()
        salaries = {
            "2022-11-10": 2956090,
            "2022-12-10": 1954940,
            "2023-01-10": 2639020,
            "2022-02-10": 1747620,
            "2023-03-10": 1855370,
            "2023-04-10": 2180580,
            "2023-05-10": 2956090,
            "2023-06-10": 1954940,
            "2023-07-10": 2639020,
            "2023-08-10": 1747620,
            "2023-09-10": 1855370,
            "2023-10-10": 2180580,
            "2023-11-10": 2004020,
        }
        events = create_events(daily_expenditure, salaries)
        
        st.title("Financial Calendar")

        
        calendar_options = calendar_options = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,dayGridYear,timeGridWeek,timeGridDay"  # Added yearly view
            },
            "displayEventTime": False,  # Disable time display
            "initialView": "dayGridMonth"  # Default view
        }

        
        state = calendar(
            events=events,
            options=calendar_options,
            custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
            """
        )

        # Default display (current month and year)
        # current_date = pd.to_datetime("today")
        # display_pie_chart(data, current_date.year, current_date.month)


        if state.get("eventClick"):
            # Extracting the selected date
            selected_date_str = state["eventClick"]["event"]["start"]
            selected_date = pd.to_datetime(selected_date_str).date()

            # Extracting viewing month and year
            viewing_month = selected_date.month
            viewing_year = selected_date.year
            viewing_date = selected_date.day

            # Filtering the data and displaying details
            details = data[data['지출일'] == pd.Timestamp(selected_date)]
            display_details(details, selected_date_str, selected_date, salaries)

            # Displaying the pie chart for the selected month and year
            display_pie_chart(data, viewing_year, viewing_month, viewing_date)
            display_graph(data)
        else:
            st.warning("Please click on a date to view details and the expenditure by category.")
        
        
    
    #button(username="fake-username", floating=True, width=221)
        


    fin_calendar()
            