import pandas as pd

Individual = pd.read_csv('../data/Individual_AV_Survey.csv')
# Stand_along = pd.read_csv('../data/Stand_alone_AV_SP_survey.csv')

# filter diagnose
# print (len(Individual))
# Individual = Individual.loc[Individual['CMSOMEW']==17]
# print (len(Individual))
# rescale agree-disagree

mode_att = ['WSAFE','PTSAFE','CARSAFE','AVSAFE','DRSAFE',
            'WCOMF','PTCOMF','CARCOMF','AVCOMF','DRCOMF',
            'WEASY', 'PTEASY', 'CAREASY', 'AVEASY', 'DREASY']

mode_att2 = ['WRELY','PTRELY','CARRELY','AVRELY','DRRELY']

for var in mode_att:
    Individual.loc[Individual[var] == 29,var] = 1
    Individual.loc[Individual[var] == 30,var] = 2
    Individual.loc[Individual[var] == 31,var] = 3
    Individual.loc[Individual[var] == 32,var] = 4
    Individual.loc[Individual[var] == 33,var] = 5
    Individual.loc[Individual[var] == 34,var] = 6
    Individual.loc[Individual[var] == 35,var] = 7
    Individual.loc[Individual[var] == 0, var] = -1

for var in mode_att2:
    Individual.loc[Individual[var] == 29,var] = 1
    Individual.loc[Individual[var] == 31,var] = 2
    Individual.loc[Individual[var] == 32,var] = 3
    Individual.loc[Individual[var] == 33,var] = 4
    Individual.loc[Individual[var] == 34,var] = 5
    Individual.loc[Individual[var] == 35,var] = 6
    Individual.loc[Individual[var] == 36,var] = 7
    Individual.loc[Individual[var] == 0, var] = -1

over_all_perception = ['WPERC','PTPERC','CARPERC','AVPERC','DRPERC']

for var in over_all_perception:
    Individual.loc[Individual[var] == 51,var] = 1
    Individual.loc[Individual[var] == 52,var] = 2
    Individual.loc[Individual[var] == 53,var] = 3
    Individual.loc[Individual[var] == 54,var] = 4
    Individual.loc[Individual[var] == 55,var] = 5
    Individual.loc[Individual[var] == 56,var] = 6
    Individual.loc[Individual[var] == 57,var] = 7
    Individual.loc[Individual[var] == 0, var] = -1

activities = ['CMACTAV','CMEFF','CMNOIMP','CMKNOWACT','CMAPPEFF','CMNOTVEH','CMNOTNOS']

for var in activities:
    Individual.loc[Individual[var] == 15,var] = 1
    Individual.loc[Individual[var] == 16,var] = 2
    Individual.loc[Individual[var] == 17,var] = 3
    Individual.loc[Individual[var] == 18,var] = 4
    Individual.loc[Individual[var] == 19,var] = 5
    Individual.loc[Individual[var] == 20,var] = 6
    Individual.loc[Individual[var] == 21,var] = 7
    Individual.loc[Individual[var] == 0, var] = -1

risk = ['UNACCRISK','LIKENEW','CAUTIOUS','DRISK','MRISK']

for var in risk:
    Individual.loc[Individual[var] == 15,var] = 1
    Individual.loc[Individual[var] == 16,var] = 2
    Individual.loc[Individual[var] == 17,var] = 3
    Individual.loc[Individual[var] == 18,var] = 4
    Individual.loc[Individual[var] == 19,var] = 5
    Individual.loc[Individual[var] == 20,var] = 6
    Individual.loc[Individual[var] == 21,var] = 7
    Individual.loc[Individual[var] == 0, var] = -1

# Select used individual characteristics
charac = ['SEX','JOB','AGE','EDU','INCOME','LICENSE','AUTOOWN','KIDUNDER18','ETH','MARRIAGE']


# Individual = Individual.loc[(Individual['UNDERS'] != -1) & (Individual['UNDERS'] != -3) ]
# lottery
lott = ['LOTT1','LOTT2','LOTT3','LOTT4']

mode_att = ['WSAFE','PTSAFE','CARSAFE','DRSAFE',
            'WCOMF','PTCOMF','CARCOMF','DRCOMF',
            'WRELY','PTRELY','CARRELY','DRRELY',
            'WEASY','PTEASY','CAREASY','DREASY']
over_all_perception = ['WPERC','PTPERC','CARPERC','DRPERC']
#activities = ['CMACTAV','CMEFF','CMNOIMP','CMNOTVEH','CMNOTNOS']
#risk = ['UNACCRISK','LIKENEW','CAUTIOUS']
ID = ['ID']
# We first extract the columns containing the indicators
columns1 =  charac + ID
print (len(Individual))
for var in charac:
    Individual = Individual.loc[Individual[var] != -1]
print (len(Individual))

columns2 = mode_att + over_all_perception
# for var in columns2:
#     Individual = Individual.loc[Individual[var] != -1]
# print (len(Individual))

columns = columns1 + columns2
Individual = Individual.loc[:,columns]
Individual.to_csv('../data/individual_new.csv', index=False)

# merge
Stand_along = pd.read_csv('../data/Stand_alone_AV_SP_survey.csv')
data = Stand_along.merge(Individual, left_on = ['ID'], right_on=['ID'])
data.to_csv('../data/data_Standalong.csv', index=False)