# Libraries
import os
os.system('cls')
import pandas as pd
import math

def octant_transition_count(mod=5000):
    try:
        df = pd.read_excel('input_octant_transition_identify.xlsx')
        #print(df.head())

        #(ua, va, wa) variables are used to store mean values of (U, V, W) columns
        ua = df.U.mean()
        va = df.V.mean()
        wa = df.W.mean()

        # df1 variable store the data frame which contains ua, va, wa values
        # df2 variable store the main data frame after concatenating df and df1
        df1 = pd.DataFrame({'U Avg':[ua],'V Avg':[va],'W Avg':[wa]})
        df2 = pd.concat([df,df1], axis = 1)
        #print(df2.head())

        # (U', V', W') columns appended to the main data frame after subtracting (ua, va, wa) from (U, V, W)
        df2["U'=U-U Avg"] = df2['U'] - ua
        df2["V'=V-V Avg"] = df2['V'] - va
        df2["W'=W-W Avg"] = df2['W'] - wa
        df2['Octant'] = None
        #print(df2.head())

        '''.loc function from pandas is used to traverse through (U', V', W') columns to append all the 
        Octant value to the Octant column'''
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 1
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]<0),'Octant'] = -1
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 2
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]<0),'Octant'] = -2
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 3
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]<0),'Octant'] = -3
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 4
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]<0),'Octant'] = -4
        #print(df2.head())

        # .astype('int') is used to convert the data type of 'Octant' column to 'int' data type
        df2['Octant'] = df2['Octant'].astype('int')

        # 8 new list are created to store the count value of {+1,-2,+2,-2,+3,-3,+4,-4}
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

        # n --> given in tut01.pdf that max value will never exceed 30000.
        n = 30000
        if n%mod == 0:
            n_ranges = n//mod
        else:
            n_ranges = math.ceil(n/mod)

        # Below while function is used to count the {+1,-2,+2,-2,+3,-3,+4,-4} values for different mod's
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
        
        # This particular part of code is used to mention the ranges of mod in the column
        c0 = []
        c0.append("Octant ID")
        c0.append("Overall Count")
        c0.append(f"Mod {mod}")
        t = 0
        u = t + mod
        for j in range(n_ranges):
            if u <= 29745:
                if t==0:
                    c0.append(f"{0000} - {u-1}")
                else:
                    c0.append(f"{t} - {u-1}")
                t = u
                u += mod
            else:
                c0.append(f"{t} - {df2.shape[0] - 1}")
                t = u
                u += mod
     
        c1 = ["+1"] + count_1
        c2 = ["-1"] + count_1_
        c3 = ["+2"] + count_2
        c4 = ["-2"] + count_2_
        c5 = ["+3"] + count_3
        c6 = ["-3"] + count_3_
        c7 = ["+4"] + count_4
        c8 = ["-4"] + count_4_

        # Final 2D list is created to store the counts of all the values 
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

        # transpose is used to convert list into columns of the 2D list
        df_final = pd.DataFrame(final_count).transpose()
        #print(df_final)

        df_final_ = pd.DataFrame(df_final.values[1:], columns=df_final.iloc[0])
        #print(df_final_)
        
        col = df_final_.columns
        #print(df_final_)
        
        oct0 = df2['Octant'].to_list()
        #print(type(oct0[0]))
        #print(len(df2['Octant']))

        n_range = n//mod
        q = 0
        r = mod

        df_final_ = gap(df_final_,col)
        final = pd.concat([df2,df_final_], axis = 1)
        #print(final.iloc[:,11:])

        final.to_excel('output_octant_transition_identify.xlsx',index = False)
    except:
        print("Error: File does not appear to exist.")
        exit()

def gap(d,col):
    g_df = []
    g0 = ["," for i in range(5)]
    g1 = [",",",",",","Overall Transition Count"," "]
    g2 = [",",",",",",",","To"]
    g_df.append(g0)
    g_df.append(g1)
    g_df.append(g2)
    for i in range(7):
        g_df.append(g0)
    g_df_final = pd.DataFrame(g_df).transpose()
    g_df_final_ = pd.DataFrame(g_df_final.values[1:], columns=col)
    #print(g_df_final_)
    x = pd.concat([d,g_df_final_],ignore_index = True)
    return x

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod=5000
octant_transition_count(mod)
print("Code Compiled Successfully")