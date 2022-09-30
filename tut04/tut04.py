#Help https://youtu.be/H37f_x4wAC0
import os
from time import time
os.system('cls')
import pandas as pd

def octant_longest_subsequence_count_with_range():
    # df = pd.read_excel('input_octant_longest_subsequence_with_range.xlsx')
    df = pd.read_excel('small_longest_subsequence_with_range - Copy.xlsx')
    #print(df.head())

    ua = df.U.mean()
    va = df.V.mean()
    wa = df.W.mean()

    df1 = pd.DataFrame({'U Avg':[ua],'V Avg':[va],'W Avg':[wa]})
    df2 = pd.concat([df,df1], axis = 1)

    #print(df2.head())

    df2["U'=U-U Avg"] = df2['U'] - ua
    df2["V'=V-V Avg"] = df2['V'] - va
    df2["W'=W-W Avg"] = df2['W'] - wa
    df2['Octant'] = None

    #print(df2.head())

    df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 1
    df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]<0),'Octant'] = -1
    df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 2
    df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]<0),'Octant'] = -2
    df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 3
    df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]<0),'Octant'] = -3
    df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 4
    df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]<0),'Octant'] = -4

    #print(df2.head())
    df2['Octant'] = df2['Octant'].astype('int')
    df2['Time'] = df2['Time'].astype('float')

    g0 = []
    for i in range(10):
        g0.append(" ")
    g1 = [" ","Count","+1","-1","+2","-2","+3","-3","+4","-4"]
    g2 = [" ","Longest Subsquence Length"]
    g2_ = []
    g3 = [" ","Count"]
    g3_ = []

    n = df2.shape[0]
    '''for i in range(n):
        x = '''

    oct = df2['Octant'].to_list()
    time1 = df2['Time'].to_list()
    l = [1,-1,2,-2,3,-3,4,-4]
    #print(oct)

    for j in l:
        count = 0
        prev = 0
        indexend = 0
        for i in range(n):
            if(oct[i] == j):
                count += 1
            else:
                if(count > prev):
                    prev = count
                    indexend = i
                count = 0
        c = 0
        count1 = 0
        for i in range(n):
            if(oct[i] != j):
                count1 = 0
            else:
                count1 += 1
                if(count1 == prev):
                    c+=1
                    count1 = 0
        #print(prev, c)
        g2_.append(prev)
        g3_.append(c)
    
    #print(g2_,g3_)
    g2 = g2 + g2_
    g3 = g3 + g3_

    g_final = []
    g_final.append(g0)
    g_final.append(g1)
    g_final.append(g2)
    g_final.append(g3)

    df_final = pd.DataFrame(g_final).transpose()
    #df_final = df_final.rename(columns=df_final.iloc[0], inplace = True)
    #print(df_final)

    df_final_ = pd.DataFrame(df_final.values[1:], columns=df_final.iloc[0])
    #print(df_final_)
    

    final = pd.concat([df2,df_final_], axis = 1)
    #print(final.iloc[:,11:])
    final.to_excel('octant_output2.xlsx', index = False)

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count_with_range()