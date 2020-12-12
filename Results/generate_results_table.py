import pandas as pd

def process_data(file_name, digit_num):


    ASC = ['ASC_PT','ASC_RIDEHAIL','ASC_DRIVE','ASC_AV']
    SE = ['BETA_Walk_Pro_Walk','BETA_PT_Pro_Walk','BETA_PT_Pro_PT','BETA_RH_Pro_RH','BETA_Drive_Pro_Drive','BETA_AV_Pro_Walk','BETA_AV_Pro_PT','BETA_AV_Pro_RH','BETA_AV_Pro_Drive']
    OE = ['BETA_Walk_Inertia_Walk','BETA_Walk_Inertia_Walk_ADJ_FRE',
          'BETA_PT_Inertia_Walk','BETA_PT_Inertia_Walk_ADJ_FRE',
          'BETA_PT_Inertia_PT','BETA_PT_Inertia_PT_ADJ_FRE',
          'BETA_RH_Inertia_RH','BETA_RH_Inertia_RH_ADJ_FRE',
          'BETA_Drive_Inertia_Drive','BETA_Drive_Inertia_Drive_ADJ_FRE',
          'BETA_AV_Inertia_Walk_ADJ_FRE',
          'BETA_AV_Inertia_PT','BETA_AV_Inertia_PT_ADJ_FRE',
          'BETA_AV_Inertia_RH','BETA_AV_Inertia_RH_ADJ_FRE',
          'BETA_AV_Inertia_Drive','BETA_AV_Inertia_Drive_ADJ_FRE']

    So = ['Income_4000_less','Income_12000_more','Single','haveLicense','Chinese','Commute','fulltimeJob','highEducation','age_60_more','age_35_less','moreThanOneCar','male','kid_under18']
    mode_seq = ['Walk','PT','RH','Drive','AV']
    alt_spec = ['BETA_WALK_WALKTIME','BETA_BUS_COST','BETA_BUS_IVTIME','BETA_BUS_WAITTIME','BETA_BUS_WALKTIME','BETA_RIDEHAIL_COST','BETA_RIDEHAIL_IVTIME','BETA_RIDEHAIL_WAITTIME',
                'BETA_DRIVE_COST','BETA_DRIVE_IVTIME','BETA_DRIVE_WALKTIME','BETA_AV_COST','BETA_AV_IVTIME','BETA_AV_WAITTIME']
    other = ['SCALE_SP',
             'Hazard_Gamma_Walk','Hazard_Gamma_PT','Hazard_Gamma_RH','Hazard_Gamma_Drive',
             'sigma_s_tidle_PT','sigma_s_tidle_RH','sigma_s_tidle_Drive','sigma_s_tidle_AV']
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
                        var_name = info[0].replace(' ','')
                        if var_in_tex != var_name:
                            continue
                        para = info[1].replace(' ','')
                        std_error = info[2].replace(' ','')
                        t_test = info[3].replace(' ','')
                        t_test = t_test.replace('-','')
                        p_value = info[4].replace(' ','')
                        para_info[var] = [para,std_error, p_value]

    data = {'var':[],'value_std_er':[]}
    for key in all_var_seq:
        if key in para_info:
            if 'sigma_s_tidle' in key:
                SIGMA_FIX_TO_BE_POSITIVE = True
            else:
                SIGMA_FIX_TO_BE_POSITIVE = False
            data['var'].append(key)
            if 'e' in para_info[key][2]:
                part1 = float(para_info[key][2].split('e')[0])
                part2 = float(para_info[key][2].split('e')[1])
                p_value_float = part1 * (pow(10,part2))
            else:
                p_value_float = float(para_info[key][2])
            if p_value_float> 0.1: #p_value
                star_str = ''
            if p_value_float <= 0.1: #p_value
                star_str = ' *'
            if p_value_float <= 0.05: #p_value
                star_str = ' **'
            if p_value_float <= 0.01: #p_value
                star_str = ' ***'

            save_value_est = round(float(para_info[key][0]),digit_num)
            save_value_std =  round(float(para_info[key][1]),digit_num)

            def process_num(save_value):
                str_ = str(save_value)
                flag_minus = False
                if '-' in str_:
                    str_ = str_.replace('-','')
                    flag_minus = True

                if len(str_) == 5: # 0.000
                    if flag_minus:
                        str_ = '-' + str_
                    if SIGMA_FIX_TO_BE_POSITIVE:
                        str_ = str_.replace('-','')
                    return str_
                elif len(str_) < 5: # need add zero
                    num_zero = 5-len(str_)
                    if flag_minus:
                        str_ = '-' + str_ + ''.join(['0'] * num_zero)
                    else:
                        str_ = str_ + ''.join(['0'] * num_zero)
                    if SIGMA_FIX_TO_BE_POSITIVE:
                        str_ = str_.replace('-','')
                    return str_
                else:
                    print('error')
                    print(str_)
                    exit()

            save_value_est = process_num(save_value_est)
            save_value_std = process_num(save_value_std)

            data['value_std_er'].append(str(save_value_est) + ' ' + '(' + str(save_value_std) + ')' + star_str)

    data = pd.DataFrame(data)
    output_name = file_name.replace('.tex','.csv')
    data.to_csv(output_name,index=False)

if __name__ == '__main__':
    file_name_list = ['Latent_Choice_seq_LV_Base.tex', 'Latent_Choice_seq_LV_only_discrete_A_PT_not_include_walk.tex',
                      'Latent_Choice_seq_LV_only_NEW_I_PT_not_include_walk.tex', 'Latent_Choice_seq_LV_A+NEW_I_PT_not_include_walk.tex']
    # file_name_list = ['Latent_Choice_seq_LV_Base.tex','Latent_Choice_seq_LV_only_discrete_A.tex', 'Latent_Choice_seq_LV_only_NEW_I.tex', 'Latent_Choice_seq_LV_A+NEW_I.tex']
    # file_name_list = ['Latent_Choice_seq_LV_only_NEW_I.tex']
    digit_num = 3
    for file_name in file_name_list:
        process_data(file_name, digit_num)
        print('finish', file_name)