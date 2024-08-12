import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import streamlit as st
import plotly.graph_objects as go
from data_exploration import explore_data
from prediction import prediction

def dashboard():
    # Page Configuration 
    # st.set_page_config(
    #     page_title='Financial Dashboard',
    #     layout='wide'
    # )

    st.title('Financial Dashboard')
    st.write("금융 정보, 예측 결과, 조언 내용 등을 한 눈에 볼 수 있습니다.")

    st.success('Selection Panel')
    page = st.selectbox(
    'Select a page to navigate: ',
    ("Visualization", "Data Exploration", "Prediction"))

    st.write('선택:', page)

    # st.write("Navigation")
    # page = st.radio("Select a page:", ["Visualization", "Data Exploration", "Prediction"])


    # Additional imports or utility functions from 'functions.py', 'Data_Exploration.py', and 'Prediction.py'
    # might be required. Adjust according to the actual code dependencies.

    # Data Loading and Preprocessing
    @st.cache_data
    def load_data():
        data = pd.read_excel("통합 문서1.xlsx")
        data['date'] = pd.to_datetime(data['지출일'], yearfirst=True)
        #data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data.set_index('date', inplace=True)

        def handle_range_values(value):
            if "-" in str(value):
                parts = str(value).split("-")
                return (int(parts[0]) + int(parts[1])) / 2
            else:
                return int(value)

        data['지출금액'] = data['지출금액'].apply(handle_range_values)
        spent_by_month = data['지출금액'].resample('M').sum()
        spent_by_month = spent_by_month.astype(float)
        spent_by_month = spent_by_month.interpolate()
        spent_by_month = spent_by_month.asfreq('M')  # Ensure frequency is set as per your use case

        
        return data, spent_by_month

    data, spent_by_month = load_data()

    # Visualization Function
    def visualize(data):
        data = data.reset_index()
        df = data.copy()
        if st.checkbox('원본 데이터 확인'):
            st.subheader('Model data')
            st.write(data)
        st.subheader('Summary Plots')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("시간에 따른 총 지출액")
            st.line_chart(data['지출금액'], use_container_width=True)

        with col2:
            st.header("카테고리별 총 지출")
            ty_plot = data['카테고리'].value_counts()
            st.bar_chart(ty_plot)
        
        df2 = df.groupby([df['date'].dt.to_period('M'), '카테고리'])['지출금액'].sum().reset_index()

        st.subheader("지출 카테고리 비교")
        clist = df2["카테고리"].unique().tolist()
        types = st.multiselect("비교하려는 지출 카테고리를 선택하세요", clist)
        st.header("You selected: {}".format(", ".join(types)))      

        dfs = {type: df2[df2["카테고리"] == type] for type in types}

        fig = go.Figure()
        for type, df2 in dfs.items():
            fig = fig.add_trace(go.Scatter(x=df2["date"], y=df2["지출금액"], name=type))

        st.plotly_chart(fig, use_container_width=True)


    def data_exploration(data):
        explore_data(data)

    def data_prediction(spent_by_month):
        prediction(spent_by_month)

    # Streamlit UI Layout and Interaction

    if page == "Visualization":
        visualize(data)
    elif page == "Data Exploration":
        data_exploration(data)
    elif page == "Prediction":
        data_prediction(spent_by_month)
