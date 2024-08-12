import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import tensorflow as tf
from statsmodels.tsa.api import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
#from sklearn.preprocessing import MinMaxScaler


def prediction(spent_by_month):
    
    y_to_train = spent_by_month['2022-06-11':'2023-06-11'] # dataset to train
    y_to_val = spent_by_month['2023-06-12':'2023-10-03'] # last X months for test  
    predict_date = len(spent_by_month) - len(spent_by_month['2023-06-12':'2023-10-03']) # the number of data points for the test set

    st.header("미래 지출 예측")

    st.subheader("모델 선택: 단순 지수 평활법 (SES)")

    ses_fit = SimpleExpSmoothing(spent_by_month, initialization_method="estimated").fit(
        smoothing_level=0.8, optimized=False
    )
    ses_forecast = ses_fit.forecast(4).rename(r"$\alpha=0.8$")
    fig, ax = plt.subplots(figsize=(8, 3))
    (line3,) = plt.plot(ses_forecast, marker="o", color="red")
    ax.plot(spent_by_month, marker="o", color="black")
    ax.plot(ses_fit.fittedvalues, marker="o", color="red")
    ax.legend([line3], [ses_forecast.name])
    st.pyplot(fig)

    st.text(ses_forecast)

    # Not a good rep bc forecast is linear so this is not a good fit for our model 
    st.subheader("모델 선택: 홀트-윈터스")


    hw_add = ExponentialSmoothing(
        spent_by_month,
        seasonal_periods=4,
        trend="add",
        seasonal="add",
        use_boxcox=True,
        initialization_method="estimated",
    ).fit()
    hw_mul = ExponentialSmoothing(
        spent_by_month,
        seasonal_periods=4,
        trend="mul",
        seasonal="mul",
        use_boxcox=True,
        initialization_method="estimated",
    ).fit()
    ax = spent_by_month.plot(
        figsize=(8, 3),
        marker="o",
        color="black",
        title="Forecasts from Holt-Winters' multiplicative method",
    )
    ax.set_ylabel("Amount Spent ($)")
    ax.set_xlabel("Month")
    hw_add.fittedvalues.plot(ax=ax, style="--", color="red")
    hw_mul.fittedvalues.plot(ax=ax, style="--", color="green")
    hw_add.forecast(12).rename("Holt-Winters (add-add-seasonal)").plot(
        ax=ax, style="--", marker="o", color="red", legend=True
    )
    hw_mul.forecast(12).rename("Holt-Winters (add-mul-seasonal)").plot(
        ax=ax, style="--", marker="o", color="green", legend=True
    )

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    # taking a look at the model metrics, comparing the HW Additive method vs the HW Multiplicative Method
    # ARIMA
    st.subheader("모델 선택: ARIMA")
    p, d, q = 5, 1, 2  # Example parameters
    model_arima = ARIMA(spent_by_month, order=(p,d,q))
    model_arima_fit = model_arima.fit()
    forecast_arima = model_arima_fit.forecast(steps=4)  # Forecast the next 4 periods
    st.line_chart(forecast_arima, use_container_width=True)

    
    # st.subheader("모델 선택: LSTM")
    
    # def create_dataset(dataset, time_step=1):
    #     dataX, dataY = [], []
    #     for i in range(len(dataset)-time_step-1):
    #         a = dataset[i:(i+time_step), 0]
    #         dataX.append(a)
    #         dataY.append(dataset[i + time_step, 0])
    #     return np.array(dataX), np.array(dataY)
    
    # scaler = MinMaxScaler(feature_range=(0,1))
    # st.write(f"Number of data points in spent_by_month: {len(spent_by_month)}")

    # spent_by_month_scaled = scaler.fit_transform(np.array(spent_by_month).reshape(-1, 1))
    
    # time_step = 3
    # X_train, y_train = create_dataset(spent_by_month_scaled, time_step)

    # # Check the shape of X_train
    # st.write(f"Shape of X_train: {X_train.shape}")

    # # Check if X_train is empty or has unexpected dimensions
    # if X_train.size == 0:
    #     st.error("X_train is empty. Check your data and preprocessing.")
    # elif len(X_train.shape) != 2:
    #     st.error("Unexpected number of dimensions in X_train. Check your data and preprocessing.")
    # else:
    #     X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

    # #X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
    
    # model_lstm = tf.keras.Sequential()
    # model_lstm.add(tf.keras.layers.LSTM(50,return_sequences=True,input_shape=(100,1)))
    # model_lstm.add(tf.keras.layers.LSTM(50,return_sequences=True))
    # model_lstm.add(tf.keras.layers.LSTM(50))
    # model_lstm.add(tf.keras.layers.Dense(1))
    # model_lstm.compile(loss='mean_squared_error',optimizer='adam')
    
    # model_lstm.fit(X_train, y_train, validation_split=0.1, epochs=100, batch_size=64, verbose=1)

    # # Prediction for next n steps
    # x_input = spent_by_month_scaled[-100:].reshape(1,-1)
    # temp_input = list(x_input)
    # temp_input = temp_input[0].tolist()
    
    # n_steps = 30  # Predict the next 30 periods
    # lst_output=[]
    # i=0
    # while(i<n_steps):
        
    #     if(len(temp_input)>100):
    #         x_input=np.array(temp_input[1:])
    #         x_input=x_input.reshape(1,-1)
    #         x_input = x_input.reshape((1, time_step, 1))
    #         yhat = model_lstm.predict(x_input, verbose=0)
    #         temp_input.extend(yhat[0].tolist())
    #         temp_input=temp_input[1:]
    #         lst_output.extend(yhat.tolist())
    #         i=i+1
    #     else:
    #         x_input = x_input.reshape((1, time_step,1))
    #         yhat = model_lstm.predict(x_input, verbose=0)
    #         temp_input.extend(yhat[0].tolist())
    #         lst_output.extend(yhat.tolist())
    #         i=i+1
    
    # day_new = np.arange(1,101)
    # day_pred = np.arange(101,131)
    
    # spent_by_month_new = spent_by_month[len(spent_by_month)-100:].append(pd.Series(lst_output), ignore_index=True)
    # st.line_chart(spent_by_month_new, use_container_width=True)



    results = pd.DataFrame(
        index=[r"$\alpha$", r"$\beta$", r"$\phi$", r"$\gamma$", r"$l_0$", "$b_0$", "SSE"]
    )
    params = [
        "smoothing_level",
        "smoothing_trend",
        "damping_trend",
        "smoothing_seasonal",
        "initial_level",
        "initial_trend",
    ]
    results["Additive"] = [hw_add.params[p] for p in params] + [hw_add.sse]
    results["Multiplicative"] = [hw_mul.params[p] for p in params] + [hw_mul.sse]
    st.dataframe(results) 

    # since multiplicative has the lowest sum of squared estimate of error we will using this method.
    with st.container():
        m = st.slider('몇개월까지 예측하시겠습니까?', 5, 10, 5)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("예측 - Additive Method")
            add_forecast = hw_add.forecast(m)
            st.dataframe(add_forecast)

        with col2:
            st.subheader("예측 - Multiplicative Method")
            mul_forecast = hw_mul.forecast(m)
            st.dataframe(mul_forecast)
