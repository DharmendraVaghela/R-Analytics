require(graphics)
require(plot3D)
require(ggplot2)
library(plot3D)
require(rgl)
require(dbscan)
library("fpc")
#install.packages("scatterplot3d")
#install.packages("plot3D")

data <- read.csv("data.csv",header=FALSE)

data2 <- data[,]
mean_data <- apply(data2,2,mean)
sd_data <- apply(data2,2,sd)
nor_data <- scale(data2,mean_data,sd_data)

#task 1:
distance <- dist(as.matrix(nor_data))
clusters <- hclust(distance)
#clusters <- hclust(dist(data[, 1:3]))
###plot(distance)
plot(clusters)

cluster_cut <- cutree(clusters,3)
#table(cluster_cut, data$X)
#plot3d(data)
plot3d(data2[,1:3],col=cluster_cut)

#task 2:

ss <- list()
clusters_k2 <- kmeans(nor_data,2)
clusters_k2
#ss[1] = clusters_k2$betweenss/clusters_k2$totss
ss[1] = clusters_k2$tot.withinss

clusters_k3 <- kmeans(nor_data,3)
clusters_k3
#ss[2] = clusters_k3$betweenss/clusters_k3$totss
ss[2] = clusters_k3$tot.withinss

clusters_k4 <- kmeans(nor_data,4)
clusters_k4 
#ss[3] = clusters_k4$betweenss/clusters_k4$totss
ss[3] = clusters_k4$tot.withinss

clusters_k5 <- kmeans(nor_data,5)
clusters_k5 
#ss[4] = clusters_k5$betweenss/clusters_k5$totss
ss[4] = clusters_k5$tot.withinss

clusters_k6 <- kmeans(nor_data,6)
clusters_k6 
#ss[4] = clusters_k5$betweenss/clusters_k5$totss
ss[5] = clusters_k6$tot.withinss


plot(2:6,ss,xlab = "K-Value", ylab = "Sum of Square Errors")
lines(2:6,ss)

plot3d(data2[,1:3],col = clusters_k4$cluster)
clusters_k4$cluster

#task 3
data2 <- data[,]
mean_data <- apply(data2,2,mean)
sd_data <- apply(data2,2,sd)
nor_data <- scale(data2,mean_data,sd_data)

#minpts = 3
kNNdistplot(nor_data, k =  3)
abline(h = 0.6, lty = 2)

db3 <- dbscan(nor_data, eps = 0.6, MinPts = 3)
plot(db3, nor_data, main = "DBSCAN", frame = FALSE)
plot3d(data2[,1:3],col=db3$cluster+1)
db3$cluster
db3

#minpts = 4
kNNdistplot(nor_data, k =  4)
abline(h = 0.65, lty = 2)

db4 <- dbscan(nor_data, eps = 0.65, MinPts = 4)
plot(db4, nor_data, main = "DBSCAN", frame = FALSE)
plot3d(data[,1:3],col=db4$cluster+1)
db4$cluster
db4

#minpts = 5
kNNdistplot(nor_data, k =  5)
abline(h = 0.7, lty = 2)

db5 <- dbscan(nor_data, eps = 0.70, MinPts = 5)
plot(db5, nor_data, main = "DBSCAN", frame = FALSE)
plot3d(data[,1:3],col=db5$cluster+1)
db5$cluster
db5

#minpts = 6
kNNdistplot(nor_data, k =  6)
abline(h = 0.8, lty = 2)

db6 <- dbscan(nor_data, eps = 0.90, MinPts = 6)
plot(db6, nor_data, main = "DBSCAN", frame = FALSE)
plot3d(data[,1:3],col=db6$cluster+1)
db6$cluster
db6


