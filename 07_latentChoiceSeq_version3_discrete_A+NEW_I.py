import pandas as pd
import numpy as np
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.distributions as dist
import biogeme.results as res
from biogeme.expressions import Beta, DefineVariable, bioDraws, log, MonteCarlo, Power


data = pd.read_csv("../data/data_Standalong_LV_NEW_I.csv")
# define variables
data['Income_4000_less'] = 0
data.loc[(data.INCOME <= 2) | (data.INCOME == 12), 'Income_4000_less'] = 1
data['Income_12000_more'] = 0
data.loc[(data.INCOME >= 7) & (data.INCOME != 12), 'Income_12000_more'] = 1
data['age_60_more'] = 0
data.loc[(data.AGE >= 60), 'age_60_more'] = 1
data['age_35_less'] = 0
data.loc[(data.AGE <= 35), 'age_35_less'] = 1
data['moreThanOneCar'] = 0
data.loc[(data.AUTOOWN > 2), 'moreThanOneCar'] = 1
data['haveLicense'] = 0
data.loc[(data.LICENSE == 1), 'haveLicense'] = 1
data['male'] = 0
data.loc[(data.SEX == 4), 'male'] = 1
data['highEducation'] = 0
data.loc[(data.EDU >= 5), 'highEducation'] = 1
data['fulltimeJob'] = 0
data.loc[(data.JOB == 1), 'fulltimeJob'] = 1
data['kid_under18'] = 0
data.loc[(data.KIDUNDER18 == 1), 'kid_under18'] = 1
data['Chinese'] = 0
data.loc[(data.ETH == 1), 'Chinese'] = 1
data['Single'] = 0
data.loc[(data.MARRIAGE == 1), 'Single'] = 1
data['Commute'] = 0
data.loc[(data.SCENARIO == 1) | (data.SCENARIO == 2), 'Commute'] = 1

data['intercept'] = 1

attitude_name = ['Pro_Walk', 'Pro_PT', 'Pro_RH', 'Pro_Drive']

for att in attitude_name:
    struc_equ_name = 'struc_equ_' + att
    data[struc_equ_name] = data[att.split('_')[1].upper() + '_LV']

# data.to_csv('data_processed.csv',index =False)

database = db.Database("stand_along", data)

globals().update(database.variables)

# exclude = (Choice == -1.0)
# database.remove(exclude)


### Variables
# Income_4000_less = DefineVariable('Income_4000_less', (INCOME<=2) + (INCOME==12),database)
# Income_12000_more = DefineVariable('Income_12000_more', (INCOME>=7)*(INCOME!=12),database)
# age_60_more = DefineVariable('age_60_more',AGE >= Numeric(60),database)
# moreThanOneCar = DefineVariable('moreThanOneCar',AUTOOWN > 2,database)
# haveLicense = DefineVariable('haveLicense',LICENSE==1,database)
# male = DefineVariable('male',SEX == 4,database)
# highEducation = DefineVariable('highEducation', EDU >= 5,database) #more than university bechelor
# fulltimeJob = DefineVariable('fulltimeJob', JOB == 1,database) #more than university bechelor
struc_equ = {}
struc_equ['Pro_Walk'] = struc_equ_Pro_Walk
struc_equ['Pro_PT'] = struc_equ_Pro_PT
struc_equ['Pro_RH'] = struc_equ_Pro_RH
struc_equ['Pro_Drive'] = struc_equ_Pro_Drive
# for att in attitude_name:
#     struc_equ_name = 'struc_equ_' + att
#     struc_equ[att] = struc_equ_


### Coefficients
### simul results
# structResults = res.bioResults(pickleFile='Seq_LatentOrdered_simul.pickle')
# structBetas = structResults.getBetaValues()
# coef = {}
# attitude_name = ['pro_motor','pro_sustain','pro_drive','risk']
# for att in attitude_name:
#     coef [att] = {}
#     for var in Variable_name:
#         var_name = 'coef_' + var + '_' + att
#         coef[att][var_name] = structBetas[var_name]


# Choice model
# choiceResults = res.bioResults(pickleFile='Latent_Choice_seq_biodraws~00.pickle')
# choiceBetas = choiceResults.getBetaValues()
choiceBetas = {}
## Latent variable: structural equation
random_variable = {}
modes_list = ['PT', 'RH', 'AV', 'Drive']
for mode in modes_list:
    random_variable[mode] = {}
    var_name = 'omega_' + mode
    # biodraws
    random_variable[mode]['omega'] = bioDraws(var_name, 'NORMAL')
    # integral
    # random_variable[mode]['omega'] = RandomVariable(var_name)
    # random_variable[mode]['omega_name'] = var_name
    # random_variable[mode]['density'] = dist.normalpdf(random_variable[mode]['omega'])
    # ----
    var_name = 'sigma_s_tidle_' + mode
    if var_name in choiceBetas:
        random_variable[mode]['sigma_s'] = Beta(var_name, choiceBetas[var_name], None, None, 0)
    else:
        random_variable[mode]['sigma_s'] = Beta(var_name, 0.0001, None, None, 0)

if len(choiceBetas) > 0:
    ASC_WALK = Beta('ASC_WALK', 0, None, None, 1)  # fixed
    ASC_PT = Beta('ASC_PT', choiceBetas['ASC_PT'], None, None, 0)
    ASC_RIDEHAIL = Beta('ASC_RIDEHAIL', choiceBetas['ASC_RIDEHAIL'], None, None, 0)
    ASC_AV = Beta('ASC_AV', choiceBetas['ASC_AV'], None, None, 0)
    ASC_DRIVE = Beta('ASC_DRIVE', choiceBetas['ASC_DRIVE'], None, None, 0)

    BETA_WALK_WALKTIME = Beta('BETA_WALK_WALKTIME', choiceBetas['BETA_WALK_WALKTIME'], None, None, 0)

    BETA_BUS_WALKTIME = Beta('BETA_BUS_WALKTIME', choiceBetas['BETA_BUS_WALKTIME'], None, None, 0)
    BETA_BUS_COST = Beta('BETA_BUS_COST', choiceBetas['BETA_BUS_COST'], None, None, 0)
    BETA_BUS_WAITTIME = Beta('BETA_BUS_WAITTIME', choiceBetas['BETA_BUS_WAITTIME'], None, None, 0)
    BETA_BUS_IVTIME = Beta('BETA_BUS_IVTIME', choiceBetas['BETA_BUS_IVTIME'], None, None, 0)

    BETA_AV_COST = Beta('BETA_AV_COST', choiceBetas['BETA_AV_COST'], None, None, 0)
    BETA_AV_WAITTIME = Beta('BETA_AV_WAITTIME', choiceBetas['BETA_AV_WAITTIME'], None, None, 0)
    BETA_AV_IVTIME = Beta('BETA_AV_IVTIME', choiceBetas['BETA_AV_IVTIME'], None, None, 0)

    BETA_RIDEHAIL_COST = Beta('BETA_RIDEHAIL_COST', choiceBetas['BETA_RIDEHAIL_COST'], None, None, 0)
    BETA_RIDEHAIL_WAITTIME = Beta('BETA_RIDEHAIL_WAITTIME', choiceBetas['BETA_RIDEHAIL_WAITTIME'], None, None, 0)
    BETA_RIDEHAIL_IVTIME = Beta('BETA_RIDEHAIL_IVTIME', choiceBetas['BETA_RIDEHAIL_IVTIME'], None, None, 0)

    BETA_DRIVE_COST = Beta('BETA_DRIVE_COST', choiceBetas['BETA_DRIVE_COST'], None, None, 0)
    BETA_DRIVE_WALKTIME = Beta('BETA_DRIVE_WALKTIME', choiceBetas['BETA_DRIVE_WALKTIME'], None, None, 0)
    BETA_DRIVE_IVTIME = Beta('BETA_DRIVE_IVTIME', choiceBetas['BETA_DRIVE_IVTIME'], None, None, 0)
    SCALE_SP = Beta('SCALE_SP', choiceBetas['SCALE_SP'], None, None, 0)
else:
    ASC_WALK = Beta('ASC_WALK', 0, None, None, 1)  # fixed
    ASC_PT = Beta('ASC_PT', 0, None, None, 0)
    ASC_RIDEHAIL = Beta('ASC_RIDEHAIL', 0, None, None, 0)
    ASC_AV = Beta('ASC_AV', 0, None, None, 0)
    ASC_DRIVE = Beta('ASC_DRIVE', 0, None, None, 0)

    BETA_WALK_WALKTIME = Beta('BETA_WALK_WALKTIME', 0, None, None, 0)

    BETA_BUS_WALKTIME = Beta('BETA_BUS_WALKTIME', 0, None, None, 0)
    BETA_BUS_COST = Beta('BETA_BUS_COST', 0, None, None, 0)
    BETA_BUS_WAITTIME = Beta('BETA_BUS_WAITTIME', 0, None, None, 0)
    BETA_BUS_IVTIME = Beta('BETA_BUS_IVTIME', 0, None, None, 0)

    BETA_AV_COST = Beta('BETA_AV_COST', 0, None, None, 0)
    BETA_AV_WAITTIME = Beta('BETA_AV_WAITTIME', 0, None, None, 0)
    BETA_AV_IVTIME = Beta('BETA_AV_IVTIME', 0, None, None, 0)

    BETA_RIDEHAIL_COST = Beta('BETA_RIDEHAIL_COST', 0, None, None, 0)
    BETA_RIDEHAIL_WAITTIME = Beta('BETA_RIDEHAIL_WAITTIME', 0, None, None, 0)
    BETA_RIDEHAIL_IVTIME = Beta('BETA_RIDEHAIL_IVTIME', 0, None, None, 0)

    BETA_DRIVE_COST = Beta('BETA_DRIVE_COST', 0, None, None, 0)
    BETA_DRIVE_WALKTIME = Beta('BETA_DRIVE_WALKTIME', 0, None, None, 0)
    BETA_DRIVE_IVTIME = Beta('BETA_DRIVE_IVTIME', 0, None, None, 0)
    SCALE_SP = Beta('SCALE_SP', 1, None, None, 0)

BETA_SOCIO = {}
modes_list = ['PT', 'RH', 'AV', 'Drive']

socio_in_U = {'Income_4000_less': Income_4000_less, 'Income_12000_more': Income_12000_more,
              'haveLicense': haveLicense, 'Single': Single, 'age_60_more': age_60_more, 'Chinese': Chinese,
              'moreThanOneCar': moreThanOneCar, 'male': male, 'fulltimeJob': fulltimeJob, 'age_35_less': age_35_less,
              'kid_under18': kid_under18,
              'Commute': Commute, 'highEducation': highEducation}

for mode in modes_list:
    BETA_SOCIO[mode] = {}
    for key in socio_in_U:
        if key == 'intercept':
            continue
        var_name = 'BETA_' + mode + '_' + key
        BETA_SOCIO[mode][var_name] = Beta(var_name, 0, None, None, 0)

BETA_ATTITUDE = {}
for att in attitude_name:
    BETA_ATTITUDE[att] = {}
    for mode in modes_list:
        beta_name = 'BETA_' + mode + '_' + att
        if beta_name in choiceBetas:
            BETA_ATTITUDE[att][mode] = Beta(beta_name, choiceBetas[beta_name], None, None, 0)
        else:
            BETA_ATTITUDE[att][mode] = Beta(beta_name, 0, None, None, 0)
    mode = 'Walk'  # add walk
    beta_name = 'BETA_' + mode + '_' + att
    if beta_name in choiceBetas:
        BETA_ATTITUDE[att][mode] = Beta(beta_name, choiceBetas[beta_name], None, None, 0)
    else:
        BETA_ATTITUDE[att][mode] = Beta(beta_name, 0, None, None, 0)

WALK_WALKTIME = DefineVariable('WALK_WALKTIME', WALKTIME, database)

BUS_WALKTIME = DefineVariable('BUS_WALKTIME', BUSWALK, database)
BUS_COST = DefineVariable('BUS_COST', BUSCOST, database)
BUS_WAITTIME = DefineVariable('BUS_WAITTIME', BUSWAIT, database)
BUS_IVTIME = DefineVariable('BUS_IVTIME', BUSIVT, database)

AV_COST = DefineVariable('AV_COST', AVCOST, database)
AV_WAITTIME = DefineVariable('AV_WAITTIME', AVWAIT, database)
AV_IVTIME = DefineVariable('AV_IVTIME', AVIVT, database)

RIDEHAIL_COST = DefineVariable('RIDEHAIL_COST', CARCOST, database)
RIDEHAIL_WAITTIME = DefineVariable('RIDEHAIL_WAITTIME', CARWAIT, database)
RIDEHAIL_IVTIME = DefineVariable('RIDEHAIL_IVTIME', CARIVT, database)

DRIVE_COST = DefineVariable('DRIVE_COST', DRIVCOST, database)
DRIVE_WALKTIME = DefineVariable('DRIVE_WALKTIME', DRIVWALK, database)
DRIVE_IVTIME = DefineVariable('DRIVE_IVTIME', DRIVIVT, database)

### DEFINITION OF UTILITY FUNCTIONS:
V_def = {'Walk': 0,
         'PT': 0,
         'RH': 0,
         'AV': 0,
         'Drive': 0}

V_def['Walk'] += ASC_WALK + \
                 BETA_WALK_WALKTIME * WALK_WALKTIME

V_def['PT'] += ASC_PT + \
               BETA_BUS_WALKTIME * BUS_WALKTIME + BETA_BUS_COST * BUS_COST + \
               BETA_BUS_WAITTIME * BUS_WAITTIME + BETA_BUS_IVTIME * BUS_IVTIME

V_def['RH'] += ASC_RIDEHAIL + \
               BETA_RIDEHAIL_COST * RIDEHAIL_COST + \
               BETA_RIDEHAIL_WAITTIME * RIDEHAIL_WAITTIME + BETA_RIDEHAIL_IVTIME * RIDEHAIL_IVTIME

V_def['AV'] += ASC_AV + \
               BETA_AV_COST * AV_COST + \
               BETA_AV_WAITTIME * AV_WAITTIME + BETA_AV_IVTIME * AV_IVTIME

V_def['Drive'] += ASC_DRIVE + \
                  BETA_DRIVE_COST * DRIVE_COST + \
                  BETA_DRIVE_WALKTIME * DRIVE_WALKTIME + BETA_DRIVE_IVTIME * DRIVE_IVTIME

for mode in modes_list:
    if mode == 'Walk':
        continue
    for key in socio_in_U:
        var_name = 'BETA_' + mode + '_' + key
        V_def[mode] += BETA_SOCIO[mode][var_name] * socio_in_U[key]

# ====================================ADD Attitude to modes==================================
mode = 'AV'
# for mode in modes_list:
for att in attitude_name:
    V_def[mode] += BETA_ATTITUDE[att][mode] * struc_equ[att]
V_def[mode] += random_variable[mode]['sigma_s'] * random_variable[mode]['omega']  # plus random

att = 'Pro_Walk'
mode = 'Walk'
V_def[mode] += BETA_ATTITUDE[att][mode] * struc_equ[att] # normalize to zero for Walk



att = 'Pro_PT'
mode = 'PT'
V_def[mode] += BETA_ATTITUDE[att][mode] * struc_equ[att]

att = 'Pro_Walk'
mode = 'PT'
V_def[mode] += BETA_ATTITUDE[att][mode] * struc_equ[att]
V_def[mode] += random_variable[mode]['sigma_s'] * random_variable[mode]['omega']  # plus random


att = 'Pro_RH'
mode = 'RH'
V_def[mode] += BETA_ATTITUDE[att][mode] * struc_equ[att]
V_def[mode] += random_variable[mode]['sigma_s'] * random_variable[mode]['omega']  # plus random

att = 'Pro_Drive'
mode = 'Drive'
V_def[mode] += BETA_ATTITUDE[att][mode] * struc_equ[att]
V_def[mode] += random_variable[mode]['sigma_s'] * random_variable[mode]['omega']  # plus random


# ====================================ADD Inertia to modes==================================
BETA_Inertia = {}
inertia_name = ['Inertia_Walk', 'Inertia_PT', 'Inertia_RH', 'Inertia_Drive']
for att in inertia_name:
    BETA_Inertia[att] = {}
    for mode in modes_list:
        beta_name = 'BETA_' + mode + '_' + att
        if beta_name in choiceBetas:
            BETA_Inertia[att][mode] = Beta(beta_name, choiceBetas[beta_name], None, None, 0)
        else:
            BETA_Inertia[att][mode] = Beta(beta_name, 0, None, None, 0)
    mode = 'Walk'  # add walk
    beta_name = 'BETA_' + mode + '_' + att
    if beta_name in choiceBetas:
        BETA_Inertia[att][mode] = Beta(beta_name, choiceBetas[beta_name], None, None, 0)
    else:
        BETA_Inertia[att][mode] = Beta(beta_name, 0, None, None, 0)

inertia_var = {}
inertia_var['Inertia_Walk'] = INERTIA_WALK
inertia_var['Inertia_PT'] = INERTIA_PT
inertia_var['Inertia_RH'] = INERTIA_RH
inertia_var['Inertia_Drive'] = INERTIA_Drive

mode = 'AV'
# for mode in modes_list:
for att in inertia_name:
    if att == 'Inertia_Walk': # we cannot add four inertia into one mode
        continue
    V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]

att = 'Inertia_Walk'
mode = 'Walk'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]

# walk to pt and pt to pt
att = 'Inertia_PT'
mode = 'PT'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]
att = 'Inertia_Walk'
mode = 'PT'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]

att = 'Inertia_RH'
mode = 'RH'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]

att = 'Inertia_Drive'
mode = 'Drive'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]






#====================================ADD hazard Inertia to modes==================================
BETA_Inertia = {}
inertia_name = ['Inertia_Walk_ADJ_FRE','Inertia_PT_ADJ_FRE','Inertia_RH_ADJ_FRE','Inertia_Drive_ADJ_FRE']
for att in inertia_name:
    BETA_Inertia[att] = {}
    for mode in modes_list:
        beta_name = 'BETA_' + mode + '_' + att
        if beta_name in choiceBetas:
            BETA_Inertia[att][mode] = Beta(beta_name,choiceBetas[beta_name], None, None, 0)
        else:
            BETA_Inertia[att][mode] = Beta(beta_name, 0, None, None, 0)
    mode = 'Walk' # add walk
    beta_name = 'BETA_' + mode + '_' + att
    if beta_name in choiceBetas:
        BETA_Inertia[att][mode] = Beta(beta_name, choiceBetas[beta_name], None, None, 0)
    else:
        BETA_Inertia[att][mode] = Beta(beta_name, 0, None, None, 0)

GAMMA_WALK = Beta('Hazard_Gamma_Walk', 0, 0, 1, 0) # bounded 0 - 1
GAMMA_PT = Beta('Hazard_Gamma_PT', 0, 0, 1, 0)
GAMMA_RH = Beta('Hazard_Gamma_RH', 0, 0, 1, 0)
GAMMA_DRIVE = Beta('Hazard_Gamma_Drive', 0, 0, 1, 0)


inertia_var = {}
inertia_var['Inertia_Walk_ADJ_FRE'] = Power(INERTIA_WALK_ADJ_FRE, 1 - GAMMA_WALK)
inertia_var['Inertia_PT_ADJ_FRE'] = Power(INERTIA_PT_ADJ_FRE, 1 - GAMMA_PT)
inertia_var['Inertia_RH_ADJ_FRE'] = Power(INERTIA_RH_ADJ_FRE, 1 - GAMMA_RH)
inertia_var['Inertia_Drive_ADJ_FRE'] = Power(INERTIA_Drive_ADJ_FRE, 1 - GAMMA_DRIVE)

mode = 'AV'
# for mode in modes_list:
for att in inertia_name:
    # if att == 'Inertia_Walk': # we cannot add four inertia into one mode # does not matter for hazard function
    #     continue
    V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]


att = 'Inertia_Walk_ADJ_FRE'
mode = 'Walk'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]


# walk to pt and pt to pt
att = 'Inertia_PT_ADJ_FRE'
mode = 'PT'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]
att = 'Inertia_Walk_ADJ_FRE'
mode = 'PT'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]


att = 'Inertia_RH_ADJ_FRE'
mode = 'RH'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]

att = 'Inertia_Drive_ADJ_FRE'
mode = 'Drive'
V_def[mode] += BETA_Inertia[att][mode] * inertia_var[att]









# deal with RP SP data
scale = (AV_AV == 0) + (AV_AV == 1) * SCALE_SP

# Associate utility functions with the numbering of alternatives
V = {1: scale * V_def['Walk'],
     2: scale * V_def['PT'],
     3: scale * V_def['RH'],
     4: scale * V_def['AV'],
     5: scale * V_def['Drive']}

# Associate the availability conditions with the alternatives.
av = {1: AV_WALK,
      2: AV_BUS,
      3: AV_CAR,
      4: AV_AV,
      5: AV_DRIVE}

# The choice model is a logit, conditional to the value of the latent variable
condprob = models.logit(V, av, CHOICE)
# --MonteCarlo
loglike = log(MonteCarlo(condprob))
# --No random
# loglike = log(condprob)
# --Integral
# condprob = Integrate(condprob * random_variable[mode]['density'], random_variable[mode]['omega_name'])
# loglike = log(condprob)
# =====

biogeme = bio.BIOGEME(database, loglike, numberOfThreads=1, numberOfDraws=2000, seed=1)
biogeme.modelName = "Latent_Choice_seq_LV_A+NEW_I"
results = biogeme.estimate()
print(f"Estimated betas: {len(results.data.betaValues)}")
print(f"Final log likelihood: {results.data.logLike:.3f}")
print(f"Output file: {results.data.htmlFileName}")
results.writeLaTeX()
print(f"LaTeX file: {results.data.latexFileName}")


