import pandas as pd
import scipy.spatial.distance as dist
import scipy.stats as ss
import numpy as np
import scipy as sp




def get_star_str(p_value_float):

    if p_value_float > 0.1:  # p_value
        star_str = ''
    if p_value_float <= 0.1:  # p_value
        star_str = ' *'
    if p_value_float <= 0.05:  # p_value
        star_str = ' **'
    if p_value_float <= 0.01:  # p_value
        star_str = ' ***'
    return star_str


def process_num(save_value,num_digits):
    num_str = num_digits+2
    str_ = str(save_value)
    flag_minus = False
    if '-' in str_:
        str_ = str_.replace('-', '')
        flag_minus = True

    if len(str_) == num_str:  # 0.000
        if flag_minus:
            str_ = '-' + str_
        return str_
    elif len(str_) < num_str:  # need add zero
        num_zero = num_str - len(str_)
        if flag_minus:
            str_ = '-' + str_ + ''.join(['0'] * num_zero)
        else:
            str_ = str_ + ''.join(['0'] * num_zero)
        return str_
    else:
        print('error')
        print(str_)
        exit()

def generate_corr_table(data):
    digit_num = 3
    data.columns = data.columns.str.upper()
    A_var = ['WALK_LV','PT_LV','RH_LV','DRIVE_LV']
    A_var_name = ['Pro-walk','Pro-PT','Pro-RH','Pro-drive']
    mode_list =['WALK','PT','RH','DRIVE']
    gamma_dict = {'WALK':0.332, 'PT':0.258, 'RH':0.283, 'DRIVE':0.607} # M4
    table_result = []

    for mode in mode_list:
        A_name = mode + '_LV'
        I_name_lag = 'INERTIA_' + mode
        I_name_har = 'INERTIA_' + mode + '_ADJ_FRE'
        A = np.array(data[A_name])
        I_lag =  np.array(data[I_name_lag])
        I_har = np.array(data[I_name_har]) ** (1-gamma_dict[mode])
        corr1, p_value1 = ss.pearsonr(A, I_lag)
        corr2, p_value2 = ss.pearsonr(A, I_har)
        star_str1 = get_star_str(p_value1)
        star_str2 = get_star_str(p_value2)

        corr1 = round(corr1, digit_num)
        corr2 = round(corr2, digit_num)
        corr1_str = process_num(corr1, digit_num)
        corr2_str = process_num(corr2, digit_num)


        results = [str(corr1_str) + star_str1,
                   str(corr2_str) + star_str2]
        table_result.append(results)

    table_save = pd.DataFrame(table_result,index=['Pro-walk','Pro-PT','Pro-RH','Pro-drive'],columns=['Inertia-lag term','Inertia-hazard term'])

    table_save.to_csv('table/corr_A_and_I.csv',index=True)


def calculate_VIF(data):
    digit_num = 3
    data.columns = data.columns.str.upper()
    A_var = ['WALK_LV','PT_LV','RH_LV','DRIVE_LV']
    A_var_name = ['Pro-walk','Pro-PT','Pro-RH','Pro-drive']
    mode_list =['WALK','PT','RH','DRIVE']
    gamma_dict = {'WALK':0.332, 'PT':0.258, 'RH':0.283, 'DRIVE':0.607} # M4
    table_result = []

    # mode = 'DRIVE'
    # I_name_lag = 'INERTIA_' + mode
    # I_name_har = 'INERTIA_' + mode + '_ADJ_FRE'
    # I_lag = np.array(data[I_name_lag])
    # I_har = np.array(data[I_name_har]) ** (1 - gamma_dict[mode])
    #
    # print(ss.pearsonr(I_lag, I_har))

    columns = []
    data_np = []
    for mode in mode_list:
        A_name = mode + '_LV'
        I_name_lag = 'INERTIA_' + mode
        I_name_har = 'INERTIA_' + mode + '_ADJ_FRE'
        columns.append(A_name)
        columns.append(I_name_lag)
        columns.append(I_name_har)

        A = np.array(data[A_name])
        I_lag =  np.array(data[I_name_lag])
        I_har = np.array(data[I_name_har]) ** (1-gamma_dict[mode])

        data_np.append(A)
        data_np.append(I_lag)
        data_np.append(I_har)

    data_np = np.array(data_np).T
    all_col_df = pd.DataFrame(data_np, columns= columns)

    data_np = all_col_df.values

    cc = sp.corrcoef(data_np, rowvar=False)
    VIF = np.linalg.inv(cc)
    vif_final = VIF.diagonal()
    vif_table = pd.DataFrame({'Var_name':columns, 'VIF_value':vif_final})
    vif_table.to_csv('table/VIF.csv',index=False)

if __name__ == '__main__':

    data = pd.read_csv("../data/data_Standalong_LV_NEW_I.csv")

    calculate_VIF(data)
