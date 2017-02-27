library(MASS)
library(leaps)

data <- read.csv("data.csv", header=TRUE)
data 

hist(data$X1)
meanx1 <- mean(data$X1)
meanx1
varx1 <- var(data$X1)
varx1


hist(data$X2)
meanx2 <- mean(data$X2)
meanx2
varx2 <- var(data$X2)
varx2


hist(data$X3)
meanx3 <- mean(data$X3)
meanx3
varx3 <- var(data$X3)
varx3


hist(data$X4)
meanx4 <- mean(data$X4)
meanx4
varx4 <- var(data$X4)
varx4


hist(data$X5)
meanx5 <- mean(data$X5)
meanx5
varx5 <- var(data$X5)
varx5

covarmatrix <- cor(data)
covarmatrix

# task 2

model = lm(data$Y~data$X1)
summary(model)
(summary(model)$sigma)**2

plot(data$Y~data$X1)
abline(model,col="blue")

resi = resid(model)

qqnorm(resi,ylab="Residuals",main="QQ Plot of Residuals") 
qqline(resi,col = "blue")
hist(resi)

plot(data$X1,resi)

predicted = predict(model)
predicted

poly_model = lm(data$Y~poly(data$X1,2,raw=T))
summary(poly_model)
(summary(poly_model)$sigma)**2

plot(data$Y~poly(data$X1,2,raw=T))
abline(model,col="blue")
#abline(poly_model,col="red")

plot(model)
abline(poly_model,col="red")

poly_resi = resid(poly_model)

qqnorm(resi,ylab="Residuals",main="QQ Plot of Residuals") 
qqline(resi,col = "blue")
qqline(poly_resi,col = "red")

# task 3
multi_model = lm(data$Y~data$X1+data$X2+data$X3+data$X4+data$X5)
summary(multi_model)
(summary(multi_model)$sigma)**2

plot(data$Y~data$X1+data$X2+data$X3+data$X4+data$X5)
abline(multi_model,col="blue")

multi_model = lm(data$Y~data$X1+data$X3+data$X4+data$X5)
summary(multi_model)
(summary(multi_model)$sigma)**2

multi_resi = resid(multi_model)

qqnorm(multi_resi,ylab="Residuals",main="QQ Plot of Residuals") 
qqline(multi_resi,col = "blue")
hist(multi_resi)

plot(data$X1+data$X3+data$X4+data$X5,multi_resi)

