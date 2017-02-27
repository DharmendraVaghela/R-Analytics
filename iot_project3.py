import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.ar_model import AR,ARResults
from statsmodels.tsa.stattools import pacf
import sys
import statsmodels.tsa.ar_model as it

def movingaverage(data,m):
    weigths = np.repeat(1.0, m)/m
    return np.convolve(data, weigths, 'valid')

def exponential_smoothing(data, alpha):
    result = [data[0]]
    for n in range(1, len(data)):
        result.append(alpha * data[n-1] + (1 - alpha) * result[n-1])
    return result

df = pd.read_csv('data.csv')


test = df[1500:]
test2 =test['X'].values.T.tolist()
train = df[:1500]
train2 =train['X'].values.T.tolist()
lowest_rmse = sys.maxint
best_m = 0
RMSE = []
M = []


for m in range(2,1500):

    sma_train = pd.DataFrame
    sma_train = movingaverage(train['X'],m)

    error = train['X'][m-1:].subtract(sma_train)

    rmse = np.sqrt(mean_squared_error(train['X'][m-1:], sma_train))
    RMSE.append(rmse)
    M.append(m)
    if rmse < lowest_rmse:
        lowest_rmse = rmse
        best_m = m

print 'Lowest RMSE for Simple moving average model:',lowest_rmse
print best_m
plt.plot(M,RMSE)
plt.xlabel('m-value')
plt.ylabel('RMSE')
plt.show()

sma_train = movingaverage(train['X'],best_m)

#plt.plot(train2[best_m-1:],'r.',sma_train,'b.')
plt.plot(train2[best_m-1:])
plt.plot(sma_train)
plt.xlabel('Range')
plt.ylabel('Original(Blue)Predicted(Green) Values')
plt.show()


#task 2
ERMSE = []
EA = []
lowest_rmse = sys.maxint
range1 = np.arange(0,1,0.1)
for a in range1:
    esm_train = pd.DataFrame
    esm_train = exponential_smoothing(train['X'],a)
    error = train['X'].subtract(esm_train)
    esm_rmse = np.sqrt(mean_squared_error(train['X'], esm_train))
    ERMSE.append(esm_rmse)
    EA.append(a)
    if esm_rmse < lowest_rmse:
        lowest_rmse = esm_rmse
        best_a = a

print 'Lowest RMSE for Exponential smoothing model:',lowest_rmse
print best_a

plt.plot(EA,ERMSE)
plt.xlabel('a-value')
plt.ylabel('RMSE')
plt.show()

esm = exponential_smoothing(train['X'],best_a)


plt.plot(train2)
plt.plot(esm)
plt.xlabel('Range')
plt.ylabel('Original(Blue)Predicted(Green) Values')
plt.show()


#task3
signal =train['X'].values.T.tolist()
model = AR(signal)
ar_res = model.fit(0)
predict = ar_res.predict()
#res = ARResults(model)
#best = model.select_order(1,'aic','c')


pacf = pacf(signal,40,'ywunbiased')
print pacf
plt.plot(pacf)
plt.xlabel('Range')
plt.ylabel('Original(Blue)Predicted(Green) Values')
plt.show()

#ar_rmse = np.sqrt(mean_squared_error(signal, predict))
#print ar_rmse
#plt.plot(pacf)
plt.plot(train2)
plt.plot(predict)
plt.xlabel('Range')
plt.ylabel('Original(Blue)Predicted(Green) Values')
plt.show()


best_m = 2
best_a = 0.1

sma_train = movingaverage(test['X'],best_m)
rmse = np.sqrt(mean_squared_error(test['X'][best_m-1:], sma_train))

print 'rmse', rmse
#plt.plot(train2[best_m-1:],'r.',sma_train,'b.')
plt.plot(test2[best_m-1:])
plt.plot(sma_train)
plt.xlabel('Range')
plt.ylabel('Original(Blue)Predicted(Green) Values')
plt.show()



esm = exponential_smoothing(test2,best_a)
esm_rmse = np.sqrt(mean_squared_error(test2, esm))

print 'esm_rmse',esm_rmse
plt.plot(train2)
plt.plot(esm)
plt.xlabel('Range')
plt.ylabel('Original(Blue)Predicted(Green) Values')
plt.show()



