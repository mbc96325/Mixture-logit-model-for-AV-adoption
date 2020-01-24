
import pandas as pd

Individual = pd.read_csv('../data/individual_new_LV.csv')

# merge

Stand_along = pd.read_csv('../data/Stand_alone_AV_SP_survey.csv')
data = Stand_along.merge(Individual, left_on = ['ID'], right_on=['ID'])
data = data.fillna(-1)
data['INERTIA_WALK'] = 0
data['INERTIA_PT'] = 0
data['INERTIA_RH'] = 0
data['INERTIA_Drive'] = 0
print(len(data))
data_RP = data.loc[data['AV_AV'] == 0].rename(columns = {'CHOICE':'CHOICE_1'})
# data_SP1 = data.loc[data['SEQ'] == 2].rename(columns = {'CHOICE':'CHOICE_2'})
# data_SP2 = data.loc[data['SEQ'] == 3].rename(columns = {'CHOICE':'CHOICE_3'})
# data_SP3 = data.loc[data['SEQ'] == 4].rename(columns = {'CHOICE':'CHOICE_4'})
# data_SP4 = data.loc[data['SEQ'] == 5].rename(columns = {'CHOICE':'CHOICE_5'})
# data_SP5 = data.loc[data['SEQ'] == 6].rename(columns = {'CHOICE':'CHOICE_6'})
# data_SP6 = data.loc[data['SEQ'] == 7].rename(columns = {'CHOICE':'CHOICE_7'})

data = data.merge(data_RP[['ID','CHOICE_1']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP1[['ID','CHOICE_2']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP2[['ID','CHOICE_3']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP3[['ID','CHOICE_4']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP4[['ID','CHOICE_5']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP5[['ID','CHOICE_6']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP6[['ID','CHOICE_7']],left_on = ['ID'], right_on = ['ID'])
print(len(data))
# some of the individuals does not have RP questions, which ara dropped

sp_name = 'CHOICE_1'
data.loc[(data['AV_AV'] != 0) & (data[sp_name] == 1), 'INERTIA_WALK'] += 1
data.loc[(data['AV_AV'] != 0) & (data[sp_name] == 2), 'INERTIA_PT'] += 1
data.loc[(data['AV_AV'] != 0) & (data[sp_name] == 3), 'INERTIA_RH'] += 1
data.loc[(data['AV_AV'] != 0) & (data[sp_name] == 5), 'INERTIA_Drive'] += 1

# sp_seq_total = 6
# for i in range(1, sp_seq_total+1):
#     for j in  range(1,i+1):
#         sp_name = 'CHOICE_' + str(j)
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 1), 'INERTIA_WALK'] += 1
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 2), 'INERTIA_PT'] += 1
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 3), 'INERTIA_RH'] += 1
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 5), 'INERTIA_Drive'] += 1

data = data.drop(columns=[sp_name])

# for i in range(0, sp_seq_total+1):
#     sp_name = 'CHOICE_' + str(i + 1)
#     data = data.drop(columns=[sp_name])
for key in ['INERTIA_WALK','INERTIA_PT','INERTIA_RH','INERTIA_Drive']:
    print(key + ' rate', len(data.loc[data[key]==1])/len(data))

data.to_csv('../data/data_Standalong_LV.csv', index=False)
print(len(data))

#==========OLD=============

# data.loc[(data['CHOICE_x'] == data['CHOICE_y']) & (data['AV_AV'] != 0),'INERTIA'] = 1
