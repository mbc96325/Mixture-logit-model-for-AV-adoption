
import pandas as pd

Individual = pd.read_csv('../data/20201016_data-LV.csv')

# merge

Stand_along = pd.read_csv('../data/Stand_alone_AV_SP_survey.csv')
data = Stand_along.merge(Individual, left_on = ['ID'], right_on=['ID'])
data = data.fillna(-1)
data['INERTIA_WALK'] = 0
data['INERTIA_PT'] = 0
data['INERTIA_RH'] = 0
data['INERTIA_Drive'] = 0
print(len(data))
data_RP = data.loc[data['AV_AV'] == 0].rename(columns = {'CHOICE':'CHOICE_RP'})
# data_SP1 = data.loc[data['SEQ'] == 2].rename(columns = {'CHOICE':'CHOICE_2'})
# data_SP2 = data.loc[data['SEQ'] == 3].rename(columns = {'CHOICE':'CHOICE_3'})
# data_SP3 = data.loc[data['SEQ'] == 4].rename(columns = {'CHOICE':'CHOICE_4'})
# data_SP4 = data.loc[data['SEQ'] == 5].rename(columns = {'CHOICE':'CHOICE_5'})
# data_SP5 = data.loc[data['SEQ'] == 6].rename(columns = {'CHOICE':'CHOICE_6'})
# data_SP6 = data.loc[data['SEQ'] == 7].rename(columns = {'CHOICE':'CHOICE_7'})

data = data.merge(data_RP[['ID','CHOICE_RP']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP1[['ID','CHOICE_2']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP2[['ID','CHOICE_3']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP3[['ID','CHOICE_4']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP4[['ID','CHOICE_5']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP5[['ID','CHOICE_6']],left_on = ['ID'], right_on = ['ID'])
# data = data.merge(data_SP6[['ID','CHOICE_7']],left_on = ['ID'], right_on = ['ID'])
print(len(data))
# some of the individuals does not have RP questions, which ara dropped

rp_name = 'CHOICE_RP'
data.loc[(data['AV_AV'] != 0) & (data[rp_name] == 1), 'INERTIA_WALK'] += 1
data.loc[(data['AV_AV'] != 0) & (data[rp_name] == 2), 'INERTIA_PT'] += 1
data.loc[(data['AV_AV'] != 0) & (data[rp_name] == 3), 'INERTIA_RH'] += 1
data.loc[(data['AV_AV'] != 0) & (data[rp_name] == 5), 'INERTIA_Drive'] += 1

# walk
mode_list = {'WALK':1,'PT':2, 'RH':3, 'AV':4, 'Drive':5}
for mode in mode_list:
    name = 'CHOICE_' + mode
    data[name] = 0
    data.loc[data['CHOICE'] == mode_list[mode], name] = 1
#
# for mode in mode_list:
#     name_2 = 'CHOICE_ADJ_' + mode
#     data[name_2] = -1
#     data.loc[data['CHOICE'] == mode_list[mode], name_2] = 1

# get fre
for mode in mode_list:
    name = 'INERTIA_' + mode + '_FRE'
    name_choice = 'CHOICE_' + mode
    data[name] = data.groupby(['ID']).cumsum()[name_choice]

# not include t (only count 0:t-1)
for mode in mode_list:
    name = 'INERTIA_' + mode + '_FRE'
    name_choice = 'CHOICE_' + mode
    data.loc[data[name_choice]==1, name] -= 1
#
# # get adj fre
for mode in mode_list:
    name = 'INERTIA_' + mode + '_ADJ_FRE'
    name_choice = 'CHOICE_ADJ_' + mode
    data[name] = 0


#
# # not include t (only count 0:t-1)
# for mode in mode_list:
#     name = 'INERTIA_' + mode + '_ADJ_FRE'
#     name_choice = 'CHOICE_ADJ_' + mode
#     data.loc[data[name_choice]==1, name] -= 1
#
# # min is zero
# for mode in mode_list:
#     name = 'INERTIA_' + mode + '_ADJ_FRE'
#     data.loc[data[name]<0, name] = 0

# a=1

ind_id_list = pd.unique(data['ID'])

count = 0
for idx in ind_id_list:
    count += 1
    print('current id', idx, 'num', count,'total', len(ind_id_list))
    used_data = data.loc[data['ID'] == idx]
    max_seq = used_data['SEQ'].max()

    for i in range(1, max_seq): # first one always zero
        for mode in mode_list:
            adj_fre = 0
            for j in range(0, i):
                if used_data['CHOICE_' + mode].iloc[j] == 1:
                    adj_fre += 1
                else:
                    adj_fre -= 1
                adj_fre = max(0, adj_fre)
            used_data['INERTIA_' + mode + '_ADJ_FRE'].iloc[i] = adj_fre
    data.loc[data['ID'] == idx,:] = used_data
    # data_new.append(used_data)

# add frequency-based inertia


# sp_seq_total = 6
# for i in range(1, sp_seq_total+1):
#     for j in  range(1,i+1):
#         sp_name = 'CHOICE_' + str(j)
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 1), 'INERTIA_WALK'] += 1
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 2), 'INERTIA_PT'] += 1
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 3), 'INERTIA_RH'] += 1
#         data.loc[(data['SEQ'] == i+1) & (data[sp_name] == 5), 'INERTIA_Drive'] += 1

data = data.drop(columns=[rp_name])
for mode in mode_list:
    name = 'CHOICE_' + mode
    data = data.drop(columns = [name])

lv_list = ['WALK_LV.ord','PT_LV.ord','RH_LV.ord','DRIVE_LV.ord']
for lv in lv_list:
    data = data.rename(columns = {lv:lv.replace('.ord','')})
    data = data.drop(columns=[lv.replace('.ord','.con')])


# for i in range(0, sp_seq_total+1):
#     sp_name = 'CHOICE_' + str(i + 1)
#     data = data.drop(columns=[sp_name])
for key in ['INERTIA_WALK','INERTIA_PT','INERTIA_RH','INERTIA_Drive']:
    print(key + ' rate', len(data.loc[data[key]==1])/len(data))

data.to_csv('../data/data_Standalong_LV_NEW_I.csv', index=False)
print(len(data))




#==========OLD=============

# data.loc[(data['CHOICE_x'] == data['CHOICE_y']) & (data['AV_AV'] != 0),'INERTIA'] = 1
