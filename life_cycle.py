import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.font_manager as fm 
import plotly.graph_objects as go

def life_cycle():
    st.title('Life Cycle Forecasting')
    st.write("AI 알고리즘을 활용한 미래 금융 상황 예측 결과를 보여줍니다")

    path = './customFonts/NanumGothic-Regular.ttf'
    font_properties = fm.FontProperties(fname=path)

    # Load the data
    data = pd.read_excel("data/life data.xls", skiprows=[0])

    # Display the column names
    data.columns.tolist()
    # Assigning column names
    column_names = [
        'Month_Year', 'Food_expenses', 'Shopping_expenses', 
        'Vehicle_maintenance_expenses', 'Cultural_life_expenses', 
        'Housing_expenses', 'Financial_insurance_expenses', 
        'Beauty_expenses', 'Transportation_expenses', 
        'Vehicle_purchase_expenses', 'Loan_expenses', 
        'Education_expenses', 'Savings', 'Others', 
        'Total_expenses', 'Total_income', 'Total_assets'
    ]

    # Re-loading the data with appropriate column names
    data = pd.read_excel("data/life data.xls", skiprows=[0], names=column_names)

    # Convert the Month_Year column to datetime type
    data['Month_Year'] = pd.to_datetime(data['Month_Year'], errors='coerce', format='%Y년 %m월') 

    # Setting the date as index
    data.set_index('Month_Year', inplace=True)


    #col1, col2 = st.columns(2)

    #with col1:
    # Plot excluding 'Total_assets' and 'Total_income'
    window_size = 10  # You can adjust this to change the amount of smoothing
    data_excluding_total_assets = data.drop(columns=['Total_assets', 'Total_income', 'Total_expenses', 'Savings'])
    data_percentage = data_excluding_total_assets.divide(data_excluding_total_assets.sum(axis=1), axis=0) * 100 
    # Calculating the rolling average for each category
    smoothed_data = data_percentage.rolling(window=window_size).mean()

    # Plotting
    plot1 = smoothed_data.plot(kind='area', colormap='Paired')
    plot1.set_xlabel('Date', fontproperties=font_properties)
    plot1.set_ylabel('Amount', fontproperties=font_properties)
    plot1.set_title('Smoothed Monthly Spending', fontproperties=font_properties)
    plot1.autoscale(enable=True, axis='x', tight=True)
    handles, labels = plot1.get_legend_handles_labels()
    plot1.legend(handles, labels, title='Category', bbox_to_anchor=(1, 1.02),
                loc='upper left', frameon=False, prop=font_properties)
    st.pyplot(plot1.figure, clear_figure=True)


    #with col2:
    # Plot only 'Total_assets' and 'Total_income'
    window_size = 8  # You can adjust this to change the amount of smoothing
    data_only_total_assets = data[['Total_assets', 'Total_income', 'Total_expenses', 'Savings']]
    data_percentage_2 = data_only_total_assets.divide(data_excluding_total_assets.sum(axis=1), axis=0) * 100 
    # Calculating the rolling average for each category
    smoothed_data_2 = data_percentage_2.rolling(window=window_size).mean()

    # Plotting
    plot2 = smoothed_data_2.plot(kind='area', colormap='viridis')  # Colormap 2
    plot2.set_xlabel('Date', fontproperties=font_properties)
    plot2.set_ylabel('Amount', fontproperties=font_properties)
    plot2.set_title('Smoothed Total Assets and Total Income', fontproperties=font_properties)
    plot2.autoscale(enable=True, axis='x', tight=True)
    handles, labels = plot2.get_legend_handles_labels()
    plot2.legend(handles, labels, title='Category', bbox_to_anchor=(1, 1.02),
                loc='upper left', frameon=False, prop=font_properties)
    st.pyplot(plot2.figure, clear_figure=True)


    st.subheader("지출 카테고리 비교")
    clist = data.columns.tolist()
    types = st.multiselect("비교하려는 지출 카테고리를 선택하세요", clist)
    st.header("You selected: {}".format(", ".join(types)))      

    dfs = {type: data[type] for type in types}
    #dfs = {type: df2[df2["카테고리"] == type] for type in types}

    window_size = 3
    fig = go.Figure()
    for expense_type, expense_data in dfs.items():
        expense_data_smoothed = expense_data.rolling(window=window_size).mean()
        fig = fig.add_trace(go.Scatter(x=expense_data.index, y=expense_data_smoothed, name=expense_type))

    st.plotly_chart(fig, use_container_width=True)




life_cycle()