
library("forecast")


data <- read.csv("data.csv",header=TRUE)
#data

train = data[1:1500,]
test = data[1500:2000,]


pacf(train)


arima <- auto.arima(train,d=0,max.q=0,max.p=3)

arima$coef

