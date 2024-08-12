import matplotlib.font_manager as fm
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# ... Other imports and code ...

# Ensure the font is available to Matplotlib
path = './customFonts/NanumGothic-Regular.ttf'
font_properties = fm.FontProperties(fname=path)
plt.rc('font', family=font_properties.get_name())


# ... Data loading and processing code ...
data = pd.read_excel("통합 문서1.xlsx")
data['date'] = pd.to_datetime(data['지출일'], yearfirst=True)

def handle_range_values(value):
    if "-" in str(value):
        parts = str(value).split("-")
        return (int(parts[0]) + int(parts[1])) / 2
    else:
        return int(value)

data['지출금액'] = data['지출금액'].apply(handle_range_values)


st.subheader('Filters')

# Filters based on unique values in your data
all_categories = ['All'] + list(data['카테고리'].unique())

categories = st.multiselect('Category', all_categories, default='All')
if 'All' in categories:
    include_categories = all_categories[1:]
else:
    include_categories = categories

col1, col2 = st.columns(2)
min_date = data['date'].min()
max_date = data['date'].max()
left_date = col1.date_input('Minimum date', min_value=min_date, value=min_date)
right_date = col2.date_input('Maximum date', max_value=max_date, value=max_date, min_value=left_date)
left_date_np = pd.Timestamp(left_date)
right_date_np = pd.Timestamp(right_date)


mask = (
    (data['카테고리'].isin(include_categories)) & 
    (data['date'] >= left_date_np) & 
    (data['date'] <= right_date_np)
)
data['Date'] = pd.to_datetime(data.date).dt.strftime('%b-%y')
filtered_data = data[mask]
if len(filtered_data) > 0:
    monthly_spend = pd.pivot_table(filtered_data, values='지출금액', columns='카테고리', index='Date', aggfunc='sum')
    
    with st.expander('Show monthly data'):
        st.subheader('Monthly data')
        st.dataframe(monthly_spend)

# Stacked area chart
plt.style.use("dark_background")
plot = monthly_spend.plot(kind='area', colormap='Paired')

# Set properties where text is involved
plot.set_xlabel('Date', fontproperties=font_properties)
plot.set_ylabel('Amount', fontproperties=font_properties)
plot.set_title('Monthly spending', fontproperties=font_properties)

# For legend labels, set font properties directly in the legend call
handles, labels = plot.get_legend_handles_labels()
plot.legend(reversed(handles), reversed(labels), title='Category', bbox_to_anchor=(1, 1.02),
            loc='upper left', frameon=False, prop=font_properties)

st.pyplot(plot.figure, clear_figure=True)
