setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
list.files()

RealEstate_California_adapted <- read.csv("RealEstate_California-adapted-new.csv")
names(RealEstate_California_adapted)
attach(RealEstate_California_adapted)

library(tidyr)

newWithoutNull <- RealEstate_California_adapted %>% 
  mutate_all(~ifelse(. %in% c("N/A", "null", ""), NA, .))

View(newWithoutNull)
summary(newWithoutNull)
nrow(newWithoutNull)


realEstateData <- newWithoutNull[complete.cases(newWithoutNull$price),]
summary(realEstateData)
realEstateData$price <- as.integer(realEstateData$price)

# Datensatz ohne Price welche einen Null wert haben
nrow(realEstateData)

priceEstateModel  = lm(price ~ bathrooms + bedrooms, data = realEstateData)
summary(priceEstateModel)


#geteilt durch 10'000 für bessere Lesbarkeit
resids <- priceEstateModel$residuals/10000
price <- realEstateData$price/10000


plot(price ~ realEstateData$bedrooms)
plot(price ~ realEstateData$bathrooms)
plot(resids~price)
mo1 <- lm(resids~price)
abline(mo1, col="red")









