library(depmixS4)
library(quantmod)
library(HMM)
library(hydroGOF)
library(gsubfn)

library("forecast")

# list[a] <- HMM(hmm,train,test,400)
# print a[0]
# 
# HMM <- function(hmm,train,test,k){
#   hmm_train = baumWelch(hmm, train)
#   hmm_simulated = simHMM(hmm_train$hmm, k)
#   predicted = strtoi(hmm_simulated$observation)
#   
#   hmm_rmse = rmse(test,predicted)
#   
#   test_mean = mean(test)
#   r_squ = sum((predicted-test_mean)^2)/sum((test-test_mean)^2)
#   
#   sse = sum((predicted-test)^2)
#   return(hmm_rmse,r_squ,sse)
# }



data = read.csv("data.csv", head=F)


train = data[1:1600,]
test = data[1601:2000,]

hmm = initHMM(c("a","b","c"),c("1","2","3","4","5"))
print(hmm)

hmm_train = baumWelch(hmm, train)
print(hmm_train$hmm)


hmm_simulated = simHMM(hmm_train$hmm, 400)
print(hmm_simulated)
predicted = strtoi(hmm_simulated$observation) # to convert the string to integer
print(predicted)

hmm_rmse = rmse(test,predicted)
print(hmm_rmse)

test_mean = mean(test)
r_squ = sum((predicted-test_mean)^2)/sum((test-test_mean)^2)
r_squ

sse = sum((predicted-test)^2)
sse

plot(test,type="o",col="blue")
lines(predicted,col="red")




#task 2


HMM <- function(hmm,train,test,k){
  hmm_train = baumWelch(hmm, train)
  hmm_simulated = simHMM(hmm_train$hmm, k)
  predicted = strtoi(hmm_simulated$observation)
  return(predicted)
}

p1 = c()
p1 = HMM(hmm,train,test,400)
print(p1)

arr_rmse= c(1:40)
arr_rsuq = c(1:40)
arr_sse = c(1:40)

min_rmse = .Machine$integer.max 
min_sse = .Machine$integer.max 
i = 0

for(k in seq(5,200,5)){
  i = i+1
  list = c()
  c = 0
  for(j in seq(0,400,k)){
    
    one = 1600+j
    training = data[1:one,]
    testing = data[one+1:2000,]
    
    pred = HMM(hmm,training,testing,k)
    
    for(x in 1:k){
      
      list[c+x] <- pred[x]
      
    }
    c = c + k
    
    
    
  }
  
  arr_rmse[i] = rmse(test,list[1:400],na.rm=TRUE)
  arr_rsuq[i] = (sum((list[1:400]-test_mean)^2))/(sum((test-test_mean)^2))
  arr_sse[i] = sum((list[1:400]-test)^2)
  
  if(arr_rmse[i] < min_rmse){
    
    min_rmse = arr_rmse[i]
    n = k
  }
  
  if(arr_sse[i]<min_sse){
    
    min_sse = arr_sse[i]
    
  }
  
  
}

print(min_sse)
print(arr_sse)
print(arr_rmse)
print(arr_rsuq)

print(min_rmse)

print(n)









# extra credit:

SMA <- function(train,v) {
  avg=0
  sma_model <- rep(v,0)
  
  for(j in (v+1):length(train)){
    for(i in 1:v){
      avg = avg + train[j-i]
    }
    sma_model = append(sma_model, avg/v)
    avg = 0
  }
  return(sma_model)
}


rmse_sma <- c(1:50)

for(i in 1:50){
  sma <- SMA(train, i)
  rmse_sma[i] <- rmse(train[i+1:2000],sma[i+1:2000])
}
rmse_sma
plot(rmse_sma)
lines(rmse_sma)


#i = 7

sma <- SMA(train, 7)
rmse_sma_min <- rmse(train[7+1:2000],sma[7+1:2000])
rmse_sma_min

sma_test <- SMA(test, 7)
rmse_test <- rmse(test[25:400],sma_test[25:400])

rmse_test

#exponential smoothing

predict = c(1,1600)
rmse = c(1:11)
p = 1
for(i in seq(0, 1, 0.1)){
  for (j in 2:1600) {
    predict[j] <- (i* train[j-1]) + ((1-i)* predict[j-1])
  }
  rmse[p] = sqrt(sum((train[2:1600] - predict[2:1600])^2)/1600)
  p = p+1
}
rmse
plot(rmse)
line(rmse)

# alpha = 0.1

predict = c(1,400)
rmse = 0
i = 0.1
for (j in 2:401) {
  predict[j] <- (i* test[j-1]) + ((1-i)* predict[j-1])
}
rmse = sqrt(sum((test[2:400] - predict[2:400])^2)/400)
rmse

#arima
pacf(train)

arima_fit <- auto.arima(train)
arima_fit

arima_fit <- auto.arima(train,d=0,max.q=0,max.p=3)
arima_fit$coef

rmse(train,fitted(arima_fit))


arima_fit <- auto.arima(test,d=0,max.q=0,max.p=3)

rmse(test,fitted(arima_fit))
arima_fit$coef
