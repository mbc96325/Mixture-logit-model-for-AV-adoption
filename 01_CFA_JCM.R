###Confirmatory Factor Analysis - Treating 7-Point Scale as Continuous (Maximum Likelihood)
#Author: Joanna Moody
#Date last modified: September 4, 2019

######################################################

#Initialization
rm(list=ls(all=TRUE))
library(lavaan)

#Load input data
setwd("/Users/jcmoody/Dropbox (MIT)/07_Latent_attitude_and_AV_perference/")
data <-read.csv("data/individual_new.csv",header=TRUE, sep = ",", stringsAsFactors = FALSE)
data[data == -1] <- NA #-1 indicates missing data


############### CONFIRMATORY FACTOR ANALYSIS ############### 
### WALK

## Model 0: Baseline model with all 5 indicators, no correlated errors 
walk.model0 <- 'Walk =~ WSAFE + WCOMF + WRELY + WEASY + WPERC' 
fit.walk.model0 <- cfa(walk.model0, data=data, missing='fiml')
summary(fit.walk.model0, fit.measures=TRUE, standardized=TRUE)
#Model fit: chi-square(N = 2003, df = 5) = 208.247, CFI = 0.939, TLI = 0.879, RMSEA = 0.142, SRMR = 0.042
#   TLI and RMSEA outside of recommended bounds
#Factor loadings: all 5 indicators have standardized loading > 0.6
mi.walk.model0 <- modindices(fit.walk.model0)
mi.walk.model0
#Modification indices: suggest that model fit could be greatly improved if the error terms 
#  of the following indicators are correlated: WSAFE ~~ WRELY are correlated (157.7); WCOMF ~~ WPERC (96.7)


## Model 1: Baseline model + correlated error between WSAFE and WRELY
walk.model1 <- 'Walk =~ WSAFE + WCOMF + WRELY + WEASY + WPERC
                WSAFE ~~ WRELY' 
fit.walk.model1 <- cfa(walk.model1, data=data, missing='fiml')
summary(fit.walk.model1, fit.measures=TRUE, standardized=TRUE)
mi.walk.model1 <- modindices(fit.walk.model1)
mi.walk.model1
#Model fit: chi-square(N = 2003, df = 4) = 50.299, CFI = 0.986, TLI = 0.966, RMSEA = 0.076, SRMR = 0.020
#  All fit indices now within recommended bounds
#Factor loadings: standardized loading for WSAFE dropped to 0.454, which is not great...
#Modification indices: MI for WCOMF ~~ WPERC fell to 47.039, so probably not worth the loss in 
#  degrees of freedom to include another correlated error term



### PUBLIC TRANSIT

## Model 0: Baseline model with all 5 indicators, no correlated errors 
pt.model0 <- 'PT =~ PTSAFE + PTCOMF + PTRELY + PTEASY + PTPERC' 
fit.pt.model0 <- cfa(pt.model0, data=data, missing='fiml')
summary(fit.pt.model0, fit.measures=TRUE, standardized=TRUE)
#Model fit: chi-square(N = 2003, df = 5) = 94.823, CFI = 0.973, TLI = 0.946, RMSEA = 0.095, SRMR = 0.028
#   Model fit is not terrible, but should inspect modification indices just in case (for slighly high RMSEA)
#Factor loadings: PTSAFE has standardized loading of 0.451, the rest are over 0.65
mi.pt.model0 <- modindices(fit.pt.model0)
mi.pt.model0
#Modification indices: Highest MIs are around 45 for PTSAFE ~~ PTEASY and PTSAFE ~~ PTPERC (probably not worth it)



### RIDEHAILING

## Model 0: Baseline model with all 5 indicators, no correlated errors 
rh.model0 <- 'RH =~ CARSAFE + CARCOMF + CARRELY + CAREASY + CARPERC' 
fit.rh.model0 <- cfa(rh.model0, data=data, missing='fiml')
summary(fit.rh.model0, fit.measures=TRUE, standardized=TRUE)
#Model fit: chi-square(N = 2003, df = 5) = 54.086, CFI = 0.988, TLI = 0.976, RMSEA = 0.070, SRMR = 0.018
#   Good model fit
#Factor loadings: All indicators have standardized loadings of > 0.65. Great!
mi.rh.model0 <- modindices(fit.rh.model0)
mi.rh.model0 #super low MIs, so no need for correlated errors (supported by already good model fit) 



### DRIVE
#Here is where we run into issues with missingness: individuals who do not have access to a car were not 
#   asked these questions; there is no way to estimate a factor score for them because they are missing on
#   all indicators systematically
#Only estimating for 953 of the 2003 individuals

## Model 0: Baseline model with all 5 indicators, no correlated errors 
drive.model0 <- 'Drive =~ DRSAFE + DRCOMF + DRRELY + DREASY + DRPERC' 
fit.drive.model0 <- cfa(drive.model0, data=data, missing='fiml')
summary(fit.drive.model0, fit.measures=TRUE, standardized=TRUE)
#Model fit: chi-square(N = 953, df = 5) = 10.634, CFI = 0.997, TLI = 0.995, RMSEA = 0.034, SRMR = 0.011
#   Ridiculously good model fit
#Factor loadings: All indicators have standardized loadings of > 0.60!
mi.drive.model0 <- modindices(fit.drive.model0)
mi.drive.model0 #super low MIs, so no need for correlated errors; can't improve model fit much over current levels!


#Have lavaan calculate R^2 for the indicators in the final model specifications
inspect(fit.walk.model1, 'r2')
inspect(fit.pt.model0, 'r2')
inspect(fit.rh.model0, 'r2')
inspect(fit.drive.model0, 'r2')

### ESTIMATE AND APPEND FACTOR SCORES
# With continuous indicators, the possible options for method = are "regression" or "Bartlett"
data$WALK_LV <- lavPredict(fit.walk.model1, type = "lv", method = "regression")
data$PT_LV <- lavPredict(fit.pt.model0, type = "lv", method = "regression")
data$RH_LV <- lavPredict(fit.rh.model0, type = "lv", method = "regression")
data$DRIVE_LV <- lavPredict(fit.drive.model0, type = "lv", method = "regression")
write.csv(data, "data/individual_new_LV.csv")


### SIMULTANEOUS ESTIMATION?
full.model <- ' Walk  =~ WSAFE + WCOMF + WRELY + WEASY + WPERC
                WSAFE ~~ WRELY
                PT =~ PTSAFE + PTCOMF + PTRELY + PTEASY + PTPERC
                RH =~ CARSAFE + CARCOMF + CARRELY + CAREASY + CARPERC
                Drive =~ DRSAFE + DRCOMF + DRRELY + DREASY + DRPERC'

fit <- cfa(full.model, data=data, missing="fiml")
summary(fit, fit.measures=TRUE, standardized=TRUE)
#Model fit is poor: chi-square(2003, 163) = 3967.0, CFI = 0.785, TLI = 0.750, RMSEA = 0.108, SRMR = 0.079
#Currently the model is using FIML to fill in for more than half of the sample missing data on the drive/
#   personal car indicators -- this is extremely suspect!

fit.listwisedelete <- cfa(full.model, data=data) #use default of listwise deletion
summary(fit.listwisedelete, fit.measures=TRUE, standardized=TRUE)
#Model fit is still poor: chi-square(953, 163) = 2381.3, CFI = 0.783, TLI = 0.747, RMSEA = 0.120, SRMR = 0.083
#I suspect there is correlation among the error terms for the same indicators across modes; we can check MIs
mi.fit.listwisedelete <- modindices(fit.listwisedelete)
mi.fit.listwisedelete 
#Modification indices:
#  Thankfully, we see very few low cross-loadings: RH =~  PTSAFE (64.7), which means our factor structure is clean
#  However, we see a lot of correlated error terms: as expected WSAFE ~~  PTSAFE (192.7), WCOMF ~~  PTCOMF (326.0), 
#     WEASY ~~ PTEASY (131.9)

#But in general, the results above suggest that we should estimate/extract the factor scores for each 
#individual from the separate CFAs rather than from the combined measurement model
