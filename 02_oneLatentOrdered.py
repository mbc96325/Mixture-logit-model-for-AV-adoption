import pandas as pd
import numpy as np
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.results as res
#import biogeme.models as models
import biogeme.loglikelihood as ll

data = pd.read_csv("../data/data_Standalong.csv")
data = data.groupby(['ID']).first().reset_index()
database = db.Database("stand_along",data)

from headers import *

# exclude = (Choice == -1.0)
# database.remove(exclude)




### Variables used in latent model
Income_4000_less = DefineVariable('Income_4000_less', (INCOME<=2) + (INCOME==12),database)
Income_12000_more = DefineVariable('Income_12000_more', (INCOME>=7)*(INCOME!=12),database)
age_60_more = DefineVariable('age_60_more',AGE >= Numeric(60),database)
age_35_less = DefineVariable('age_35_less',AGE <= Numeric(35),database)
moreThanOneCar = DefineVariable('moreThanOneCar',AUTOOWN > 2,database)
haveLicense = DefineVariable('haveLicense',LICENSE==1,database)
male = DefineVariable('male',SEX == 4,database)
highEducation = DefineVariable('highEducation', EDU >= 5,database) #more than university bechelor
fulltimeJob = DefineVariable('fulltimeJob', JOB == 1,database) #more than university bechelor
kid_under18 = DefineVariable('kid_under18', KIDUNDER18 == 1,database)
Chinese = DefineVariable('Chinese', ETH == 1,database)
Single = DefineVariable('Single', MARRIAGE == 1,database)
Commute = DefineVariable('Commute', (SCENARIO == 1)+ (SCENARIO == 2),database)


variable_dict = {'age_60_more': age_60_more, 'Chinese': Chinese,'highEducation': highEducation,
                 'male': male,
                 'fulltimeJob': fulltimeJob, 'age_35_less': age_35_less, 'kid_under18': kid_under18,
                 'Commute': Commute, 'intercept': 1}
# variable_dict = {'Income_4000_less':Income_4000_less,'Income_12000_more':Income_12000_more,'age_60_more':age_60_more,
#                  'moreThanOneCar':moreThanOneCar,'male':male,'highEducation':highEducation,
#                  'fulltimeJob':fulltimeJob,'age_35_less':age_35_less, 'kid_under18':kid_under18,'Chinese':Chinese,
#                  'Single':Single,'Commute':Commute,'intercept':1}
Variable_name = [key for key in variable_dict]
# variable_dict = {'haveLicense':haveLicense,}

### Coefficients

# old results
# structResults = res.bioResults(pickleFile='Seq_LatentOrdered_pro_sustain_old.pickle')
# structBetas = structResults.getBetaValues()
structBetas = {}

coef = {}
attitude_name = ['Pro_Walk','Pro_PT','Pro_RH','Pro_Drive']
for att in attitude_name:
    coef [att] = {}
    for var in Variable_name:
        var_name = 'coef_' + var + '_' + att
        if var_name not in structBetas:
            coef[att][var_name] = Beta(var_name, 0, None, None, 0)
        else:
            coef[att][var_name] = Beta(var_name,structBetas[var_name],None,None,0)
        #coef[att][var_name] = Beta(var_name, 0, None, None, 0)


### Latent variable: structural equation

struc_equ = {}
for att in attitude_name:
    struc_equ[att] = 0
    for var in Variable_name:
        coef_name = 'coef_' + var + '_' + att
        struc_equ[att] += variable_dict[var] * coef[att][coef_name]



### Measurement equations
# indicators = {'pro_motor':[CARSAFE,CARCOMF,CARRELY,CAREASY,CARPERC],
#               'pro_sustain':[WSAFE,PTSAFE,PTCOMF,WCOMF,PTRELY,WRELY,PTEASY,WEASY,PTPERC,WPERC],
#               'pro_drive':[DRSAFE,DRCOMF,DRRELY,DREASY,DRPERC],
#               'risk':[UNACCRISK,LIKENEW,CAUTIOUS]}

indicators = {'Pro_Walk':[WSAFE, WCOMF, WRELY, WEASY, WPERC],
              'Pro_PT':[PTSAFE,PTCOMF,PTRELY,PTEASY,PTPERC],
              'Pro_RH':[CARSAFE,CARCOMF,CARRELY,CAREASY,CARPERC],
              'Pro_Drive':[DRSAFE,DRCOMF,DRRELY,DREASY,DRPERC]}
INTER_dict={}
B_Factor = {}
for key in indicators: 
    
    INTER_dict[key] = []
    B_Factor[key] = []
    count = 0
    for ind in indicators[key]:
        count += 1
        var_name1 = 'INTER_' + ind.name + '_' + key
        var_name2 = 'B_' + ind.name + '_' + key
        if count == 1: # set the first intercept to 0 (normalize), first beta to 1; 1 means increase of this factor lead to increase of indicators
            INTER_dict[key].append(Beta(var_name1, 0,None,None, 1))
            B_Factor[key].append(Beta(var_name2, 1, None, None, 1))
        else:
            if var_name1 in structBetas and var_name2 in structBetas:
                INTER_dict[key].append(Beta(var_name1, structBetas[var_name1], None, None, 0))
                B_Factor[key].append(Beta(var_name2, structBetas[var_name2], None, None, 0))
            else:
                INTER_dict[key].append(Beta(var_name1, 0, None, None, 0))
                B_Factor[key].append(Beta(var_name2, 1, None, None, 0))

Ordinal_U_dict = {}
for key in indicators:
    Ordinal_U_dict[key] = []
    for idx in range(len(indicators[key])):
        Ordinal_U_dict[key].append(INTER_dict[key][idx] + B_Factor[key][idx] * struc_equ[key])

SIGMA_STAR_dict = {}
for key in indicators:
    count = 0
    SIGMA_STAR_dict[key] = []
    for ind in indicators[key]:
        count += 1
        var_name1 = 'SIGMA_STAR_' + ind.name + '_' + key
        if count == 1:
            SIGMA_STAR_dict[key].append(Beta(var_name1, 1, None, None, 1))
        else:
            if var_name1 in structBetas:
                SIGMA_STAR_dict[key].append(Beta(var_name1, structBetas[var_name1], None, None, 0))
            else:
                SIGMA_STAR_dict[key].append(Beta(var_name1, 1, None, None, 0))
#print (SIGMA_STAR_dict)
delta_dict = {}
tau_dict = {}
for key in indicators:
    delta_dict[key] = {}
    delta_name1 = 'delta_1'+'_'+key
    if delta_name1 in structBetas:
        delta_dict[key]['delta_1'] = Beta(delta_name1, structBetas[delta_name1], 0, 10, 0)
    else:
        delta_dict[key]['delta_1'] = Beta(delta_name1, 0.1, 0, 10, 0)
    delta_name2 = 'delta_2' + '_' + key
    if delta_name1 in structBetas:
        delta_dict[key]['delta_2'] = Beta(delta_name2, structBetas[delta_name2], 0, 10, 0)
    else:
        delta_dict[key]['delta_2'] = Beta(delta_name2, 0.2, 0, 10, 0)
    delta_name3 = 'delta_3' + '_' + key
    if delta_name3 in structBetas:
        delta_dict[key]['delta_3'] = Beta(delta_name3, structBetas[delta_name3], 0, 10, 0)
    else:
        delta_dict[key]['delta_3'] = Beta(delta_name3, 0.3, 0, 10, 0)
    tau_dict[key] = {}
    tau_dict[key]['tau_1'] = -delta_dict[key]['delta_1'] -delta_dict[key]['delta_2'] -delta_dict[key]['delta_3']
    tau_dict[key]['tau_2'] = -delta_dict[key]['delta_1'] -delta_dict[key]['delta_2']
    tau_dict[key]['tau_3'] = -delta_dict[key]['delta_1']
    tau_dict[key]['tau_4'] = delta_dict[key]['delta_1']
    tau_dict[key]['tau_5'] = delta_dict[key]['delta_1'] + delta_dict[key]['delta_2']
    tau_dict[key]['tau_6'] = delta_dict[key]['delta_1'] + delta_dict[key]['delta_2'] + delta_dict[key]['delta_3']


P_indicator = {}
for key in indicators:
    P_indicator[key] = []
    for idx in range(len(indicators[key])):
        U_tau_1 = (tau_dict[key]['tau_1'] - Ordinal_U_dict[key][idx]) / SIGMA_STAR_dict[key][idx]
        U_tau_2 = (tau_dict[key]['tau_2'] - Ordinal_U_dict[key][idx]) / SIGMA_STAR_dict[key][idx]
        U_tau_3 = (tau_dict[key]['tau_3'] - Ordinal_U_dict[key][idx]) / SIGMA_STAR_dict[key][idx]
        U_tau_4 = (tau_dict[key]['tau_4'] - Ordinal_U_dict[key][idx]) / SIGMA_STAR_dict[key][idx]
        U_tau_5 = (tau_dict[key]['tau_5'] - Ordinal_U_dict[key][idx]) / SIGMA_STAR_dict[key][idx]
        U_tau_6 = (tau_dict[key]['tau_6'] - Ordinal_U_dict[key][idx]) / SIGMA_STAR_dict[key][idx]
        Indicat = {
            1: bioNormalCdf(U_tau_1),
            2: bioNormalCdf(U_tau_2) - bioNormalCdf(U_tau_1),
            3: bioNormalCdf(U_tau_3) - bioNormalCdf(U_tau_2),
            4: bioNormalCdf(U_tau_4) - bioNormalCdf(U_tau_3),
            5: bioNormalCdf(U_tau_5) - bioNormalCdf(U_tau_4),
            6: bioNormalCdf(U_tau_6) - bioNormalCdf(U_tau_5),
            7: 1 - bioNormalCdf(U_tau_6),
            -1: 1
        }
        P_indicator[key].append(Elem(Indicat, indicators[key][idx]))

# estimate seperately
# for key in indicators:
#     #key = 'pro_sustain'
#     loglike = 0
#     for idx in range(len(indicators[key])):
#         loglike += log(P_indicator[key][idx])
#     biogeme  = bio.BIOGEME(database = database, formulas = loglike, numberOfThreads = 8, numberOfDraws = 3000, seed= 1)
#     biogeme.modelName = "Seq_LatentOrdered_" + key
#     results = biogeme.estimate()
#     print(f"Estimated betas: {len(results.data.betaValues)}")
#     print(f"final log likelihood: {results.data.logLike:.3f}")
#     print(f"Output file: {results.data.htmlFileName}")
#     results.writeLaTeX()
#     print(f"LaTeX file: {results.data.latexFileName}")


# estimate simultaneously
loglike = 0
for key in indicators:
    for idx in range(len(indicators[key])):
        loglike += log(P_indicator[key][idx])

biogeme  = bio.BIOGEME(database = database, formulas = loglike, numberOfThreads = 8, numberOfDraws = 2000, seed= 2)
biogeme.modelName = "Seq_LatentOrdered_simul"
results = biogeme.estimate()
print(f"Estimated betas: {len(results.data.betaValues)}")
print(f"final log likelihood: {results.data.logLike:.3f}")
print(f"Output file: {results.data.htmlFileName}")
results.writeLaTeX()
print(f"LaTeX file: {results.data.latexFileName}")