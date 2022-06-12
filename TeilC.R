library(readxl)
#library(readr)
RealEstate_California_adapted <- read_excel("Documents/FH/Sem2/WDDA/RealEstate_California-adapted.xlsx", 
                                            sheet = "Tabelle1")
#RealEstate_California_adapted = read.csv("Documents/FH/Sem2/WDDA/RealEstate_California-adapted.xlsx")

attach(RealEstate_California_adapted)

install.packages(tidyr)
library(tidyr)

newWithoutNull <- RealEstate_California_adapted %>% 
  mutate_all(~ifelse(. %in% c("N/A", "null", ""), NA, .))

View(newWithoutNull)
nrow(newWithoutNull)


data <- newWithoutNull[complete.cases(newWithoutNull$price),]

# Datensatz ohne Price welche einen Null wert haben
nrow(data)

model1  = lm(price ~ bathrooms + bedrooms, data = data)
plot(model1$residuals)

#TODO: more plots to explain the model

summary(model1)


resid(model1)



