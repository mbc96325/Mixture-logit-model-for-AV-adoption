import pandas as pd

file_name = 'Latent_Choice_seq_LV_A+I~00.tex'

ASC = ['ASC_PT','ASC_RIDEHAIL','ASC_DRIVE','ASC_AV']
SE = ['BETA_Walk_Pro_Walk','BETA_PT_Pro_Walk','BETA_PT_Pro_PT','BETA_RH_Pro_RH','BETA_Drive_Pro_Drive','BETA_AV_Pro_Walk','BETA_AV_Pro_PT','BETA_AV_Pro_RH','BETA_AV_Pro_Drive']
OE = ['BETA_Walk_Inertia_Walk','BETA_PT_Inertia_Walk','BETA_PT_Inertia_PT','BETA_RH_Inertia_RH','BETA_Drive_Inertia_Drive','BETA_AV_Inertia_PT','BETA_AV_Inertia_RH','BETA_AV_Inertia_Drive']
So = ['Income_4000_less','Income_12000_more','Single','haveLicense','Chinese','Commute','fulltimeJob','highEducation','age_60_more','age_35_less','moreThanOneCar','male','kid_under18']
mode_seq = ['Walk','PT','RH','Drive','AV']
alt_spec = ['BETA_WALK_WALKTIME','BETA_BUS_COST','BETA_BUS_IVTIME','BETA_BUS_WAITTIME','BETA_BUS_WALKTIME','BETA_RIDEHAIL_COST','BETA_RIDEHAIL_IVTIME','BETA_RIDEHAIL_WAITTIME',
            'BETA_DRIVE_COST','BETA_DRIVE_IVTIME','BETA_DRIVE_WALKTIME','BETA_AV_COST','BETA_AV_IVTIME','BETA_AV_WAITTIME']
other = ['SCALE_SP','sigma_s_tidle_PT','sigma_s_tidle_RH','sigma_s_tidle_Drive','sigma_s_tidle_AV']
Sociald = []
for mode in mode_seq:
    for var in So:
        name = 'BETA_' + mode + '_' + var
        Sociald.append(name)

all_var_seq = ASC + SE + OE + alt_spec + Sociald + other

para_info = {}

flag = 0
with open(file_name) as fin:
    for line in fin:
        if '\\section{Parameter estimates}' in line:
            flag = 1
        if '\\end{tabular}' in line and flag == 1:
            flag = 0
            print(line)
            break
        if flag == 1:
            for var in all_var_seq:
                var_in_tex = var.replace('_','\\_')
                if var_in_tex in line:
                    info = line.split('&')
                    para = info[1].replace(' ','')
                    t_test = info[3].replace(' ','')
                    t_test = t_test.replace('-','')
                    para_info[var] = [para,t_test]

data = {'var':[],'value_t-test':[]}
for key in all_var_seq:
    if key in para_info:
        data['var'].append(key)
        data['value_t-test'].append(para_info[key][0] + ' ' + '(' + para_info[key][1] + ')')

data = pd.DataFrame(data)
output_name = file_name.replace('.tex','.csv')
data.to_csv(output_name,index=False)