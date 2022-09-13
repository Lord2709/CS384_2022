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
        #print(count_4_)

        c_0 = [" ", " ","User Input"]
        for i in range(n_ranges):
            c_0.append(" ")
    
        c0 = []
        c0.append("Octant ID")
        c0.append("Overall Count")
        c0.append(f"Mod {mod}")
        c0.append(f"0000 - {mod}")
        t = mod
        u = t + mod
        for j in range(3,n_ranges+2):
            if u <= 30000:
                p = 0
                p = f"{t+1} - {u}" 
                c0.append(p)
                t = u
                u = u + mod
            else:
                p = 0
                p = f"{t+1} - {30000}" 
                c0.append(p)
                t = u
                u = u + mod
        #print(c0)

        c1 = [1]
        c1 += count_1

        c2 = [-1]
        c2 += count_1_

        c3 = [2]
        c3 += count_2

        c4 = [-2]
        c4 += count_2_

        c5 = [3]
        c5 += count_3

        c6 = [-3]
        c6 += count_3_

        c7 = [4]
        c7 += count_4

        c8 = [-4]
        c8 += count_4_

        #print(c0)
        final_count = []
        final_count.append(c_0)
        final_count.append(c0)
        final_count.append(c1)
        final_count.append(c2)
        final_count.append(c3)
        final_count.append(c4)
        final_count.append(c5)
        final_count.append(c6)
        final_count.append(c7)
        final_count.append(c8)

        df_final = pd.DataFrame(final_count).transpose()
        #print(df_final)

        df_final_ = pd.DataFrame(df_final.values[1:], columns=df_final.iloc[0])
        #print(df_final_)
        
        final = pd.concat([df2,df_final_], axis = 1)
        #print(final.iloc[:,11:])

        final.to_csv('octant_output.csv',index = False)
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