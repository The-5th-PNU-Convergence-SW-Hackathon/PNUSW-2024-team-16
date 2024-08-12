import streamlit as st
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def seasonal_decompose (y):
    decomposition = sm.tsa.seasonal_decompose(y, model='additive',extrapolate_trend='freq', period=1)
    fig = decomposition.plot()
    fig.set_size_inches(14,7)
    st.pyplot(fig)

def test_stationarity(timeseries, title):
    
    #Determing rolling statistics
    rolmean = pd.Series(timeseries).rolling(window=12).mean() 
    rolstd = pd.Series(timeseries).rolling(window=12).std()
    
    fig, ax = plt.subplots(figsize=(16, 4))
    ax.plot(timeseries, label= title)
    ax.plot(rolmean, label='rolling mean')
    ax.plot(rolstd, label='rolling std (x10)')
    ax.legend()
    st.pyplot(fig)
    pd.options.display.float_format = '{:.8f}'.format

def ADF_test(timeseries, dataDesc):
    st.text(' {} 정상성 테스트 결과'.format(dataDesc))
    dftest = adfuller(timeseries.dropna(), autolag='AIC')
    st.text('Test statistic = {:.3f}'.format(dftest[0]))
    st.text('P-value = {:.3f}'.format(dftest[1]))
    st.text('Critical values :')
    for k, v in dftest[4].items():
        st.text('\t{}: {} - The data is {} stationary with {}% confidence'.format(k, v, 'not' if v<dftest[0] else '', 100-int(k[:-1])))
