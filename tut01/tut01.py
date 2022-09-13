import os
os.system('cls')
import pandas as pd
import math

def octact_identification(mod=5000):
    try:
        df = pd.read_csv('octant_input.csv')
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

        count_1 = []
        count_1_ = []
        count_2 = []
        count_2_ = []
        count_3 = []
        count_3_ = []
        count_4 = []
        count_4_ = []

        count_1.append((df2['Octant'] == 1).value_counts()[1])
        count_1.append(" ")
        count_1_.append((df2['Octant'] == -1).value_counts()[1])
        count_1_.append(" ")
        count_2.append((df2['Octant'] == 2).value_counts()[1])
        count_2.append(" ")
        count_2_.append((df2['Octant'] == -2).value_counts()[1])
        count_2_.append(" ")
        count_3.append((df2['Octant'] == 3).value_counts()[1])
        count_3.append(" ")
        count_3_.append((df2['Octant'] == -3).value_counts()[1])
        count_3_.append(" ")
        count_4.append((df2['Octant'] == 4).value_counts()[1])
        count_4.append(" ")
        count_4_.append((df2['Octant'] == -4).value_counts()[1])
        count_4_.append(" ")
        #print(count_1,count_1_)

        n = 30000
        if n%mod == 0:
            n_ranges = n//mod
        else:
            n_ranges = math.ceil(n/mod)

        k = 0
        m = mod
        n_r = n_ranges
        while n_r > 0:   
            n_r -= 1
            d_f = df2.iloc[k:m]
            count_1.append((d_f['Octant'] == 1).value_counts()[1])
            count_1_.append((d_f['Octant'] == -1).value_counts()[1])
            count_2.append((d_f['Octant'] == 2).value_counts()[1])
            count_2_.append((d_f['Octant'] == -2).value_counts()[1])
            count_3.append((d_f['Octant'] == 3).value_counts()[1])
            count_3_.append((d_f['Octant'] == -3).value_counts()[1])
            count_4.append((d_f['Octant'] == 4).value_counts()[1])
            count_4_.append((d_f['Octant'] == -4).value_counts()[1])
            k = m 
            m = m + mod
        print(count_4_)
    except:
        print("Error: File does not appear to exist.")
        exit()

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod=5000
octact_identification(mod)