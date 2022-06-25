# Teil 2

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
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

library(readxl)
california <- read_excel("california.xls", sheet="19tbl08ca")
head(california)

View(california)
View(data)


joined_df <- merge(data, california, by.x = "city", 
                   by.y = "City", all.x = TRUE, all.y = FALSE)

View(joined_df)


model2  = lm(price ~ bathrooms + bedrooms + Crimerate, data = joined_df)

confint(model2)
summary(model2)


plot(price ~ bathrooms + bedrooms)
