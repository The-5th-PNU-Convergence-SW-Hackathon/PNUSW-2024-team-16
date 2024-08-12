import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def simulation():

    class Loan(object):
        def __init__(self, principle, rate, term_months):
            self.principle = principle
            self.rate = rate
            self.term_months = term_months
            self.interest_paid = 0.0
            self.term_months = term_months
            self.time_left = term_months
            self.payment_monthly = self.payment()
            self.offset = 0
        
        def payment(self):
            return self.principle/d(self.rate, self.term_months)
        
        def current_interest(self):
            return self.rate/1200.0 * (self.principle - self.offset)
    
        def make_payment(self, amount):
            interest = self.current_interest()
            self.interest_paid += min(interest, amount)
            self.principle -= max(0, amount - interest)
            return interest

    def d(r, n):
        r = r/1200.0
        return (np.power(1+r, n) -1)/(r*np.power(1+r, n))

    
    def make_figure(results, offset=True):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x=[z['month']/12 for z in results], 
                                y=[z['principle'] for z in results],
                        hovertemplate = '%{x:.1f} years<br>\nPrinciple: %{y:₩,.0f}<extra></extra>',
                        mode='lines+markers',
                        name='Principle remaining'))
        fig.add_trace(go.Scatter(x=[z['month']/12 for z in results], 
                                y=[z['interest_paid'] for z in results],
                        hovertemplate = '%{x:.1f} years<br>\nInterest: %{y:₩,.0f}<extra></extra>',
                        mode='lines+markers',
                        name='Interest paid'))
        if offset:
            fig.add_trace(go.Scatter(x=[z['month']/12 for z in results], 
                                y=[z['offset'] for z in results],
                        mode='lines+markers',
                        hovertemplate = '%{x:.1f} years<br>\nOffset: %{y:₩,.0f}<extra></extra>',
                        name='Offset account balance'))

        fig.update_layout(
            width=1100, height=600,
                    xaxis_title="Years",
        yaxis_title="Loan value",
        font = {"size": 14},
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.6
        ),
        # hovermode="x unified" ,
            # font_family="Courier New",
            # font_color="blue",
            # title_font_family="Times New Roman",
            # title_font_color="red",
            # legend_title_font_color="green"
        )

        return fig

    
    def scenario(rate, principle, payment, cash_left=0, offset_average=0):
        loan = Loan(principle, rate, 30*12)
        loan.offset = offset_average
        results = []
        for m in range(12*30):
            i = loan.make_payment(payment)
            results.append([loan.principle, loan.interest_paid, i])
            if loan.principle <= 0:
                break    
                

    
    def scenario2(rate, principle, income=0, start_cash=0, expenses=2500, reserve=1500, offset=True):
        loan = Loan(principle, rate, 30*12)
        if offset:
            loan.offset = start_cash
        results = []
        for m in range(12*30):
            payment = income - expenses - reserve
            if offset:
                loan.offset += reserve
            i = loan.make_payment(payment)
            results.append({"month": m, "principle": loan.principle, "interest_paid": loan.interest_paid, "offset": loan.offset})
            if loan.principle <= 0 or loan.principle <= loan.offset:
                break    
        return results

    
    def load_stamps():
        return pd.read_csv("stamps_korea.csv")

    
    def calc_stamp_duty(state, house_cost):
        duty = 0
        info = ""
        stamps = load_stamps()
        stamps = stamps[stamps.state == state]
        for i, row in stamps.iterrows():
            if house_cost < row['max']:
                duty = row['constant'] + .01*row['percent']*(house_cost-row['subtract'])
        if house_cost < 1000000:
            duty *= 0.75
            info = "discount applied"
        return int(duty), info


    # def nope():
    #     duty = 0
    #     message = ""
    #     if state == "Vic":
    #         if house_cost < 1000000:
    #             duty = int(0.75 * (0.055 * house_cost))
    #             message = "discount applied"
    #         else:
    #             duty = int((0.055 * house_cost))
    #     elif state == "NSW":
    #         if house_cost < 1033000:
    #             duty = int(9285 + .045*(house_cost - 310000))
    #         else:
    #             duty = (41820 + .055*(house_cost - 1033000))

    #     else:
    #         duty = .04*house_cost
    #         message = "Not real value"

    #     return int(duty), message

    st.title('금융자산 시뮬레이터')
    st.write("미래의 금융 상황을 시뮬레이션해 보세요.")


    col1, col2 = st.columns(2)
    # Wrapping markdown with a div and applying the CSS class
    st.markdown("## 주택 및 대출")

    with col1:
        house_cost = st.slider('주택 비용 (천원)', value=100000, min_value=30000, max_value=2000000, step=5000)
        province = st.selectbox("지역:", ["서울", "경기", "부산", "대구", "인천", "광주", "대전", "울산"], index=1)
        # Your calculation function here
        # stamp_duty, info = calc_stamp_duty(state, house_cost)  
        stamp_duty, info = calc_stamp_duty(province, house_cost)
        star = "" if len(info) == 0 else "*"
        st.markdown(f"인지세: ₩{stamp_duty:,}{star}")
        cash = st.number_input('전체 현금 (천원)', value=20000, step=5000)
        
    with col2:
        borrow = st.slider("대출 금액 (천원)", value=house_cost + stamp_duty - cash, min_value=50000, max_value=house_cost, step=10000)
        cash_left = cash - house_cost - stamp_duty + borrow 
        lvr = borrow/house_cost

        st.markdown(f"남은 현금: ₩{cash_left:,}  --  LVR: {lvr*100:.1f}%")
        rate = st.slider("이자율", value=2.6, min_value=2.0, max_value=5.0, step=.1)
        term = st.radio("기간", [20, 25, 30], index=2)
        offset = st.radio("Offset", ['Yes', 'No'], index=0)

        if len(info) > 0:
            st.markdown(f"*{info}")

    loan = Loan(borrow, rate, term*12)
    income = st.number_input("월별 순수입 (천원)", value=3000, step=500)
    expenses = st.number_input("월별 지출 (천원)", value=1000, step=100)
    st.markdown(f"월별 최소 지불금: **₩{int(loan.payment_monthly):,}**")
    reserve = st.slider("예비 현금 (월별) - 가능한 경우 오프셋 계좌에 들어갑니다", min_value=0, max_value=int(income-expenses-loan.payment_monthly), step=500)

    results = scenario2(rate, borrow, income=income, start_cash=cash_left, expenses=expenses, reserve=reserve, offset=(offset=="Yes"))
    st.markdown(f"### {len(results)/12:.1f} 년 안에 상환합니다. 총 이자 지불: ₩{int(results[-1]['interest_paid'])*1000:,}")
    fig = make_figure(results, offset=(offset=="Yes"))

    st.plotly_chart(fig)






