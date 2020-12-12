import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

colors = colors = sns.color_palette('muted')

def plot_correlation_matrix_raw(data, col):
    # Generate a large random dataset
    d = data.loc[:,col]

    # Compute the correlation matrix
    corr = d.corr()

    # Generate a mask for the upper triangle
    # mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 9))

    # sns.set_theme(style="white")
    sns.heatmap(corr,annot=True,fmt='.1g', square=True ,cmap= 'coolwarm',cbar_kws={"shrink": .82})

    plt.show()

def get_num_of_questions(question_comb, data, save_fig):

    ## only sp without car
    question_comb_used = question_comb.loc[(question_comb['Q_ID']!= -1)&(question_comb['VIVT'] == -1)]
    print("num_pax", len(pd.unique(question_comb_used['ID'])))
    question_comb_used['num_questions'] = 1
    num_questions = question_comb_used.groupby(['Q_ID']).sum()['num_questions'].reset_index(drop=False)

    print("total num questions", sum(num_questions['num_questions']))
    num_rows = len(data)
    print('observations', len(data))
    scale = num_rows/sum(num_questions['num_questions'])
    num_questions['num_questions'] *= scale
    num_questions['num_questions'] = np.round(num_questions['num_questions'])

    add_num = num_rows - sum(num_questions['num_questions'])

    print('add_num', add_num)

    if add_num>0:
        num_questions = num_questions.sort_values(['num_questions'])
        num_questions['num_questions'].iloc[0] -= add_num
    elif add_num < 0:
        num_questions = num_questions.sort_values(['num_questions'])
        num_questions['num_questions'].iloc[-1] += add_num


    num_questions = num_questions.sort_values(['Q_ID'])
    diff_num = num_rows - sum(num_questions['num_questions'])
    # print(diff_num)
    assert num_rows == sum(num_questions['num_questions'])

    month_count_plot = list(num_questions['num_questions'])

    mean_ = np.mean(num_questions['num_questions'])
    std_ = np.std(num_questions['num_questions'])
    print('mean', mean_)
    print('std',std_)
    ################ plot
    N = len(month_count_plot)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.5      # the width of the bars
    fig, ax = plt.subplots(figsize=(15, 6))
    rects1 = ax.bar(ind, month_count_plot, width, color=colors[4])
    # rects2 = ax.bar(ind+width, density_2015, width, color=colors[1])
    labels_list = ['Q' + str(i+1) for i in range(27)]
    plt.yticks(fontsize=16)
    plt.ylim(0,620)
    plt.xlim(ind[0]-1,ind[-1]+1)
    #ax.set_yticklabels([str(i) + '%' for i in range(40, 61, 10)])
    ax.set_ylabel('Number of replicated times',fontsize=16)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels_list,fontsize=16)
    ax.set_xlabel('Question ID',fontsize=15)
    x = [ind[0]-1,ind[-1]+1]
    plt.plot(x,[mean_, mean_],'k--', label = 'Mean')

    plt.legend(fontsize=16)
    plt.tight_layout()
    if save_fig == 0:
        plt.show()
    else:
        plt.savefig('question_replicated_times.png', dpi=200)


def plot_correlation_matrix_level(question_comb,save_fig):
    # Generate a large random dataset
    question_comb_used = question_comb.loc[(question_comb['Q_ID']!= -1)&(question_comb['VIVT'] == -1)]
    question_comb_used = question_comb_used.drop(columns = ['Q_ID','SEQ','ID','VCost','VWalk','VIVT'])

    question_comb_used = question_comb_used.rename(columns = {'WT':'Walk time','PTCost': 'PT Cost',
                                                              'PTWalk': 'PT walk time', 'PTWait': 'PT wait time','PTIVT': 'PT in-veh time',
                                                              'CCost': 'RH cost', 'CWait': 'RH wait time','CIVT': 'RH in-veh time',
                                                              'ACost': 'AV cost', 'AWait': 'AV wait time','AIVT': 'AV in-veh time',})


    corr = question_comb_used.corr()

    max_corr = 0
    for k in range(len(corr)):
        used_data = np.hstack([corr.iloc[k,0:k].values, corr.iloc[k, k+1:].values])
        max_temp = np.max(np.abs(used_data))
        if max_temp > max_corr:
            max_corr = max_temp


    print('max corr', np.round(max_corr, 2))

    f, ax = plt.subplots(figsize=(10, 9))

    # sns.set_theme(style="white")
    sns.heatmap(corr,annot=True,fmt='.1g', square=True ,cmap= 'coolwarm',cbar_kws={"shrink": .82})

    plt.tight_layout()
    if save_fig == 0:
        plt.show()
    else:
        plt.savefig('empirical_corr.png', dpi=200)

if __name__ == '__main__':
    col_dict = {'PT':['BUSCOST','BUSWALK','BUSWAIT','BUSIVT'],
                'RH':['CARCOST','CARWAIT','CARIVT'],
                'AV':['AVCOST','AVWAIT','AVIVT'],
                'Drive':['DRIVCOST', 'DRIVWALK','DRIVIVT']}

    data = pd.read_csv("../data/data_Standalong_LV_NEW_I.csv")
    question_comb = pd.read_csv('preprocess/Stand_alone_AV_SP_survey_Question_comb.csv')

    # plot_correlation_matrix_raw(data,col = col_dict['Drive'])

    # get_num_of_questions(question_comb, data, save_fig = 1)

    plot_correlation_matrix_level(question_comb,save_fig = 1)