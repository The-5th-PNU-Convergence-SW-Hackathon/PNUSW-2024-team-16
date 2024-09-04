import streamlit as st
import openai
import pandas as pd
import numpy as np
import datetime
import collections
import calendar
#from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import altair as alt
from fin_calendar import dispaly_calendar
from chatbot import chatbot
from dashboard import dashboard
from visualize import visualize
from simulation import simulation
from life_cycle import life_cycle
from portfolio import portfolio

def show_financial_advisor():

    #st.title("DGB IM Calendar")
    st.markdown("<h1 style='text-align: center; color: skyblue'>🗓️ DGB IM Calendar 🗓️</h1>", unsafe_allow_html=True)
    
    st.sidebar.write("설문조사에 기반한 상품 추천 목록입니다")
    st.sidebar.image("https://github.com/JinukHong/shadowFunk/assets/45095330/05b20da2-93c0-422c-a731-965b3b6c806a", use_column_width=True)
    st.sidebar.image("https://github.com/JinukHong/shadowFunk/assets/45095330/c12f207a-0e76-48e8-84b8-afeccb50258c", use_column_width=True)

    tab1, tab2, tab3,tab4, tab5, tab6  = st.tabs(["사용자 프로필 설정", "데이터 수집 및 분석", "통합 대시보드", "미래 금융 예측", "시뮬레이션 기능", "포트폴리오 추천"])

    if 'adjusted_income' not in st.session_state:
        st.session_state.adjusted_income = 0
    if 'adjusted_expense' not in st.session_state:
        st.session_state.adjusted_expense = 0


    with tab1:
        dispaly_calendar()
        # st.header("사용자 프로필 설정")
        # age = st.number_input("나이를 입력하세요:", min_value=0, max_value=150, step=1)
        # job = st.text_input("직업을 입력하세요:")
        # income = st.number_input("월별 수입을 입력하세요(만원):")
        # family_members = st.number_input("가족 구성원 수를 입력하세요:", min_value=0, step=1)
        # future_plan = st.multiselect("미래의 계획을 선택하세요:", ["결혼", "자녀 양육", "집 구입", "기타"])
        chatbot()
        
    with tab2:
        st.header("데이터 수집 및 분석")
        st.write("연결된 금융 계좌에서의 입출금 내역, 카드 사용 내역 등을 실시간으로 수집 및 분석")
        visualize()
                                
    with tab3:
        dashboard()

    with tab4:
        life_cycle()
        # if st.button("예측 시작"):
        #     data = pd.DataFrame({
        #         'Category': ['Income', 'Expense'],
        #         'Amount': [st.session_state.adjusted_income, st.session_state.adjusted_expense]  # Use session_state values
        #     })
        #     chart = alt.Chart(data).mark_bar().encode(
        #         x='Category',
        #         y='Amount',
        #         color='Category'
        #     ).properties(width=400)

        #     st.altair_chart(chart, use_container_width=True)
        
    with tab5:
        simulation()
            # Update session_state values
            # st.session_state.adjusted_income = st.slider("월 소득 조정:", 0, 10000000, st.session_state.adjusted_income)
            # st.session_state.adjusted_expense = st.slider("월 지출 조정:", 0, 5000000, st.session_state.adjusted_expense)

            # if st.button("시뮬레이션 실행"):
            #     st.write("시뮬레이션 결과를 보여줍니다 ...")
            #     data = pd.DataFrame({
            #         'Category': ['Income', 'Expense'],
            #         'Amount': [st.session_state.adjusted_income, st.session_state.adjusted_expense]
            #     })
            #     chart = alt.Chart(data).mark_bar().encode(
            #         x='Category',
            #         y='Amount',
            #         color='Category'
            #     ).properties(width=400)

            #     st.altair_chart(chart, use_container_width=True)

    with tab6:
        portfolio()
    
    # with tab6:
    #     st.header("AI Secretary Chatbot")
        # user_message = st.text_input("Ask the AI Secretary:")

        # if user_message:
        #     # Collecting user's information
        #     user_info = f"User's Age: {age}, Job: {job}, Monthly Income(krw): {income*10000}, Family Members: {family_members}, Future Plan: {', '.join(future_plan)}"

        #     # Provide a default system message for context
        #     system_message = f"You are an AI financial advisor. {user_info}"

        #     # Simulate API call (uncomment when using the real OpenAI API)
        #     with st.spinner("Waiting for the AI Secretary's response..."):
        #         completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        #                                                 messages=[
        #                                                     {"role": "system", "content": system_message},
        #                                                     {"role": "user", "content": user_message}
        #                                                 ])
        #         response = completion.choices[0].message.content
        #         # response = "This is a simulated response. Integrate with OpenAI API for real responses."  # Placeholder
        #     st.write(f"AI Secretary: {response}")

    

    