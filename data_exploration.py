import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
# Import any other functions you might need, e.g., seasonal_decompose, test_stationarity, ADF_test
from functions import seasonal_decompose, test_stationarity, ADF_test

def explore_data(data):
    st.header("📈 데이터 탐색")
    st.markdown("시계열 모델링을 위한 데이터 탐색")
    st.subheader("월별 총 소비와 월별 평균 resample")

    # This is monthly spending and mean resampling on monthly basis
    #data_sliced = data['2022-06-11':'2023-10-03']

    fig, ax = plt.subplots(figsize=(20, 6))

    ax.plot(data['지출금액'],marker='.', linestyle='-', linewidth=0.5, label='Monthly')
    ax.plot(data['2022-06-11':'2023-10-03'].resample('M').mean(),marker='o', markersize=8, linestyle='-', label='Monthly Mean Resample')
    ax.set_ylabel('Total Spent')
    ax.legend()
    st.pyplot(fig)
    with st.expander("Read more"):
        st.markdown("이 플롯을 사용하면 월별 기준으로 소비를 시각화하고 그 달의 평균 소비량과 비교할 수 있습니다. 결과에 영향을 줄 수 있는 패턴을 확인하고 사용할 예측 모델을 결정하는 데 중요합니다. 평균 선의 안정성에 따라 개인의 소비 변동성을 판단할 수 있습니다.")

    st.subheader("Decomposition")
    st.markdown("먼저 모델에서 패턴을 찾기 시작합니다. 이를 위해 선형 시각화 후에 복잡성을 더 볼 수 있게 데이터를 분해합니다. 이 함수는 시계열 데이터의 네 가지 일반적인 패턴인 관측, 추세, 계절성, 잔차로 데이터를 분해하는 데 도움이 됩니다.")

    df = pd.DataFrame(data['지출금액'])
    seasonal_decompose(df)

    
    # Stationarity - must check if data is stationary 
    ### plot for Rolling Statistic for testing Stationarity

    st.subheader("Stationarity")
    st.markdown("다음으로 데이터의 정상성을 확인합니다. 데이터의 통계적 특성이 시간이 지나도 크게 변하지 않을 때 데이터는 정상입니다. 정확한 예측을 위해 시계열 예측 모델을 구축할 때 정상 데이터를 갖는 것이 중요합니다. 시각화와 Augmented Dickey-Fuller (ADF) 테스트를 사용하여 정상성을 확인합니다.")

    test_stationarity(df['지출금액'],'raw data')
    with st.expander("Read more"):
        st.markdown("test_stationarity 함수를 사용하면 시간이 지나면서 표준 편차가 얼마나 급격하게 변하는지 한눈에 알 수 있어 rolling statistics (평균과 분산)를 볼 수 있습니다. 평균과 표준 편차가 시간이 지나도 크게 변하지 않으므로 정상적이라고 가정할 수 있지만, 확실한 정보를 위해 ADF를 사용합니다.")
    
    # Augmented Dickey-Fuller Test

    st.subheader("Augmented Dickey-Fuller Test")
    ADF_test(df,'raw data')
    with st.expander("Read more"):
        st.markdown("ADF 테스트를 통해 데이터가 정상적이라는 것을 확신할 수 있습니다.")
