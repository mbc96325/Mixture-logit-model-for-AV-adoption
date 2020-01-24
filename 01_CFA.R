rm(list=ls(all=TRUE))
library(lavaan)

# read file
setwd("D:/Baichuan Mo/Dropbox (MIT)/00_Research/07_Latent_attitude_and_AV_perference/")
data <-read.csv("data/individual_new.csv",header=TRUE, sep = ",", stringsAsFactors = FALSE)
out_put_name = 'CFA_mode_based.csv'

HS.model <- ' Walk  =~ WSAFE + WCOMF + WRELY + WEASY + WPERC
              PT =~ PTSAFE + PTCOMF + PTRELY + PTEASY + PTPERC
              RH =~ CARSAFE + CARCOMF + CARRELY + CAREASY + CARPERC
              Drive =~ DRSAFE + DRCOMF + DRRELY + DREASY + DRPERC'

fit <- cfa(HS.model, data=data, 
           std.lv=TRUE,  
           missing="fiml")

fit

summary(fit, fit.measures=TRUE, standardized=TRUE)
#-----------------second dimention-------------
# HS.model <- ' Safe  =~ WSAFE + PTSAFE + CARSAFE + DRSAFE
#               Comf =~ WCOMF + PTCOMF + CARCOMF + DRCOMF
#               Easy =~ WEASY + PTEASY + CAREASY + DREASY
#               Rely =~ WRELY + PTRELY + CARRELY+ DRRELY
#               Perc =~ WPERC + PTPERC + CARPERC + DRPERC'
# 
# fit <- cfa(HS.model, data=data, 
#            std.lv=TRUE,  
#            missing="fiml")
# 
# fit
# 
# summary(fit, fit.measures=TRUE, standardized=TRUE)