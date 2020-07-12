#%%
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

os.chdir("/home/skystone/Documents/TimeSeries")
df = pd.read_csv('T1.csv', delimiter=',')

#%%

dataset = df[['Date/Time','Wind Speed (m/s)']]
dataset = dataset.rename(columns = {"Date/Time" :"timeStamp","Wind Speed (m/s)":"windSpeed"})
dataset = dataset[:5000]

# MISSING DATA POINTS
# 2018-01-26 06:20:00  to  2018-01-30 14:40:00
# 2018-09-28 21:20:00  to  2018-10-02 16:30:00
# 2018-11-10 21:10:00  to  2018-11-14 12:00:00

newTime = []
for i in dataset['timeStamp']:
    # YYYY-MM-DD HH:MM:SS   => Required
    # DD MM YYYY HH:MM      => my format
    #print("{0}-{1}-{2} {3}:00".format(i[6:10],i[3:5],i[:2],i[11:16]))
    newTime.append(i[6:10] + "-" + i[3:5] + "-" + i[:2] + " " + i[11:16] + ":00")
dataset['timeStamp'] = newTime


#%%

dataset.index = pd.to_datetime(dataset.timeStamp)
# dataset.index = pd.DatetimeIndex(dataset.index).to_period('H')
dataset.index = pd.DatetimeIndex(dataset.index)
dataset = dataset.drop('timeStamp', axis=1)

dataset.plot()

dataset = dataset.sort_index()
dataset.fillna(df.mean())

#%%

# Testing whether there are null values
dataset[dataset.isnull()]
len(dataset[dataset.isnull()])
dataset = dataset.sort_index()
dataset.index

#%%

# Replacing NaN values with the previous effective data
dataset.windSpeed.fillna(method='pad', inplace=True)
dataset[dataset.windSpeed.isnull()]

dataset.describe()

#%%

dataset['Ticks'] = range(0,len(dataset.index.values))
#dataset = dataset.drop('Ticks', axis=1)

#very simple plotting
fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Ticks')
ax1.set_ylabel('windSpeed')
ax1.set_title('Original Plot')
ax1.plot('Ticks', 'windSpeed', data = dataset);

#%%

from statsmodels.tsa.stattools import adfuller
def stationarity_check(ts):    
    # Determing rolling statistics
    #roll_mean = pd.rolling_mean(ts, window=12)
    roll_mean = ts.rolling(12).mean()
    
    # Plot rolling statistics:
    plt.plot(ts, color='green',label='Original')
    plt.plot(roll_mean, color='blue', label='Rolling Mean')
    plt.legend(loc='best')
    plt.title('Rolling Mean')
    plt.show(block=False)
    
    # Perform Augmented Dickey-Fuller test:
    print('Augmented Dickey-Fuller test:')
    df_test = adfuller(ts)
    print("type of df_test: ",type(df_test))
    print("df_test: ",df_test)
    df_output = pd.Series(df_test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    print("df_output: \n",df_output)
    for key,value in df_test[4].items():
        df_output['Critical Value (%s)'%key] = value
    print(df_output)
    
stationarity_check(dataset.windSpeed)

#%%

#dfIndia['Roll_Mean'] = pd.rolling_mean(dfIndia.AverageTemperature, window=12)
dataset['Roll_Mean'] = dataset.windSpeed.rolling(12).mean()
dataset.windSpeed.rolling(12)

from statsmodels.graphics.tsaplots import plot_pacf,plot_acf
plot_acf(dataset.windSpeed, lags=50)
plot_pacf(dataset.windSpeed, lags=50)
plt.xlabel('lags')
plt.show()

#%%

from statsmodels.tsa.arima_model import ARMA

import itertools
p = q = range(0, 4)
pq = itertools.product(p, q)
for param in pq:
    try:
        mod = ARMA(dataset.windSpeed,order=param)
        results = mod.fit()
        print('ARMA{} - AIC:{}'.format(param, results.aic))
    except:
        continue
    
model = ARMA(dataset.windSpeed, order=(3,3))  
results_MA = model.fit(method="css-mle")  

#%%

plt.plot(dataset.windSpeed)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('Fitting data _ MSE: %.2f'% (((results_MA.fittedvalues-dataset.windSpeed)**2).mean()))
plt.show()

#%%
#Check

from pandas.tseries.offsets import DateOffset
future_dates=[dataset.index[-1]+ DateOffset(months=x)for x in range(0,24)]

future_datest_df=pd.DataFrame(index=future_dates[1:],columns=dataset.columns)

future_datest_df.tail()

future_df=pd.concat([dataset,future_datest_df])

# future_df['forecast'] = results_MA.predict(start = 104, end = 120, dynamic= True)
future_df['forecast'] = results_MA.predict('2019-10-09')  
#future_df[['Sales', 'forecast']].plot(figsize=(12, 8))

#%%

#predictions = results_MA.predict('2018-03-02 18:50:00')
predictions = results_MA.predict('4000')
predictions

#%%

from sklearn.externals import joblib 
joblib.dump(results_MA, 'humidityModel.pkl') 