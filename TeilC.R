setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
list.files()

RealEstate_California_adapted <- read.csv("RealEstate_California-adapted-new.csv")
names(RealEstate_California_adapted)
attach(RealEstate_California_adapted)

install.packages(tidyr)
library(tidyr)

newWithoutNull <- RealEstate_California_adapted %>% 
  mutate_all(~ifelse(. %in% c("N/A", "null", ""), NA, .))

View(newWithoutNull)
summary(newWithoutNull)
nrow(newWithoutNull)


data <- newWithoutNull[complete.cases(newWithoutNull$price),]

# Datensatz ohne Price welche einen Null wert haben
nrow(data)

model1  = lm(price ~ bathrooms + bedrooms, data = data)
summary(model1)

plot(price)


plot(resid(model1) ~ predict(model1))

nrow(model1)
plot(resid(model1))

plot(model1$residuals, xlim=c(0,30))

plot(model1)

hist(model1$residuals + mean(model1~price), xlim=c(0,30))



plot(bedrooms~bathrooms)
plot(price~bathrooms)




library(datasauRus)

head(model1)

library(datasauRus)
if(requireNamespace("dplyr")){
  suppressPackageStartupMessages(library(dplyr))
  datasaurus_dozen %>%
    group_by(price) %>%
    summarize(
      mean_x = mean(price),
      mean_y = mean(bathrooms),
      std_dev_x = sd(price),
      std_dev_y = sd(bathrooms),
      corr_x_y = cor(price, bathrooms)
    )
}
if (require(ggplot2)) {
  library(ggplot2)
  library(datasauRus)
  ggplot(datasaurus_dozen, aes(x = x, y = y, colour = dataset)) +
    geom_point() +
    theme_void() +
    theme(legend.position = "none") +
    facet_wrap( ~dataset, ncol = 3)
}











library(scatterplot3d)
s3d <- scatterplot3d(x=bedrooms, y=bathrooms, z=as.numeric(price)/1000000, 
              zlab="Preis geteilt durch 1 Million", xlab="Schlafzimmer", ylab="Badzimmer",
              highlight.3d = TRUE, angle = 40, box = FALSE)

s3d <- scatterplot3d(c(bedrooms, bathrooms, price), 
                     zlab="Preis geteilt durch 1 Million", xlab="Schlafzimmer", ylab="Badzimmer",
                     highlight.3d = TRUE, angle = 40, box = FALSE)

library(rgl)
library(car)
scatter3d(x=bathrooms, z=bedrooms, y=as.numeric(price))


my.lm <- (as.numeric(model1$price) ~ model1$bathrooms ~ model1$bedrooms)
s3d$plane3d(my.lm)

library(addgrids3d)
addgrids3d(model1)
s3d$plane3d(model1, lty.box = "solid")


??scatterplot

scatterplot3d(x=TV, y=radio, z=sales, scale.y=0.9, angle = 30)

s3d <- scatterplot3d(data, type="h", highlight.3d=TRUE,
              angle=55, scale.y=0.7, pch=16, main="scatterplot3d - 5")





b = coef(model1)
f = function(price){b[1] + b[2]*price + b[3]*price^2}
pbf <- function(x,y){B[[1]]+B[[2]]*x+B[[3]]*y}
curve(f(price), add=TRUE, col="red")

# plot(model1$residuals)
# abline(0,0)

#TODO: more plots to explain the model

summary(model1)


resid(model1)






# Teil 2

library(readxl)
california <- read_excel("california.xls", sheet="19tbl08ca")
head(california)

View(california)
View(data)

total <- merge(data , california, by="city")


joined_df <- merge(data, california, by.x = "city", 
                   by.y = "City", all.x = TRUE, all.y = FALSE)

View(joined_df)


model2  = lm(price ~ bathrooms + bedrooms + Crimerate, data = joined_df)

confint(model2)
summary(model2)





