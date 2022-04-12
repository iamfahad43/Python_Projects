import os, time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import math
##notice that the excel file must be inside a "result" folder
import statsmodels
from statsmodels.stats.proportion import proportion_confint
import numpy as np


def plot_graph(excel_file_name, title):
    os.chdir(str(os.getcwd()+"/result"))
    MyFinalResult = pd.read_excel(excel_file_name)

    filename =title + ".png"
    image = MyFinalResult["logMar"].to_list()
    result = str(os.getcwd())

    combine = []
    logmar = MyFinalResult["logMar"].to_list()
    user_responses = MyFinalResult["user_resp"].to_list()
    image_order = MyFinalResult["Image_Order"].to_list()

    percentage_of_2, percentage_of_3 = 0, 0

    for n, order in enumerate(image_order):
        if order=="1_3_2_":
            if user_responses[n] == 2:
               user_responses[n] = 3
               percentage_of_3 += 1
            elif user_responses[n] == 3:
               user_responses[n] = 2
               percentage_of_2 += 1
            else:
                pass
        else:
            if user_responses[n] == 2:
                percentage_of_2 += 1
            else:
                percentage_of_3 += 1

    percentage_of_2 = str(round(percentage_of_2*100/len(image_order), 2))
    percentage_of_3 = str(round(percentage_of_3*100/len(image_order), 2))
    print(percentage_of_2)

    values_dic = {}
    numbers_dic = {}
    for count, log in enumerate(logmar):
        name = str(str(log)+"_"+str(user_responses[count]))
        if any(key==name for key in values_dic):
            values_dic[name] += 1
            numbers_dic[log] += 1
        else:
            values_dic[name] = 1
            numbers_dic[log] = 1

    copy_dic = dict(values_dic)
    binomial = {}
    for key in values_dic:
        stripped = str(key)[:-2]
        try:
            n_2=int(copy_dic[str(stripped+"_2")])
        except:
            n_2=0
        try:
            n_3=int(copy_dic[str(stripped+"_3")])
        except:
            n_3=0
        div = int(n_2+n_3)
        print(div)
        values_dic[key] = round((float(copy_dic[key]*100)/div), 2)
        low, up = proportion_confint(float(copy_dic[key]), div, alpha=0.05, method="wilson")
        binomial[key] = [low*100, up*100]

    for key in values_dic:
        x_value = str(key)[:-2]
        x=round(float(x_value), 2)
        y=round(float(values_dic[key]), 2)
        low, up = binomial[key]
        err_up = up - y
        err_down = y - low
        print([err_up, err_down], y, low, up)
        if str(key)[-1] == "2":
            plt.errorbar(x, y, yerr=np.array([[err_down], [err_up]]), xerr=0, fmt='o', color="blue", ecolor='blue', elinewidth=3, capsize=4)
        else:
            plt.errorbar(x, y, yerr=np.array([[err_down], [err_up]]), xerr=0, fmt='o', color="red", ecolor='red', elinewidth=3, capsize=4)

    plt.title('Which is closer to method R0')
    plt.xlabel(str(' LogMAR '))
    plt.ylabel('% User Response')
    plt.savefig(str('Plot_'+filename))
    plt.show()


