#Help https://youtu.be/H37f_x4wAC0
import os
os.system('cls')
import pandas as pd

def octant_longest_subsequence_count():
    try:
        df = pd.read_excel('input_octant_longest_subsequence.xlsx')
        # print(df.head())

        ua = df.U.mean()
        va = df.V.mean()
        wa = df.W.mean()

        df1 = pd.DataFrame({'U Avg':[ua],'V Avg':[va],'W Avg':[wa]})
        df2 = pd.concat([df,df1], axis = 1)

        # print(df.head())

        df2["U'=U-U Avg"] = df2['U'] - ua
        df2["V'=V-V Avg"] = df2['V'] - va
        df2["W'=W-W Avg"] = df2['W'] - wa
        df2['Octant'] = None

        # print(df2.head())

        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 1
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]<0),'Octant'] = -1
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 2
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]>=0) & (df2["W'=W-W Avg"]<0),'Octant'] = -2
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 3
        df2.loc[(df2["U'=U-U Avg"]<0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]<0),'Octant'] = -3
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]>=0),'Octant'] = 4
        df2.loc[(df2["U'=U-U Avg"]>=0) & (df2["V'=V-V Avg"]<0) & (df2["W'=W-W Avg"]<0),'Octant'] = -4

        # print(df2.head())
        # print(df2.info())
        df2['Octant'] = df2['Octant'].astype('int')

        g0 = []
        for i in range(11):
            g0.append(" ")
        g1 = [" ","Count","+1","-1","+2","-2","+3","-3","+4","-4"]
        g2 = [" ","Longest Subsquence Length"]
        g2_ = []
        g3 = [" ","Count"]
        g3_ = []

        n = df2.shape[0]
        oct = df2['Octant'].to_list()
        int_l = [1,-1,2,-2,3,-3,4,-4]


        '''count1 to store initial count and previous_count is used to store 
        previous count as the count value keeps on changing.'''
        for j in int_l:
            count1 = 0
            previous_count = 0
            for i in range(n):
                if(oct[i] == j):
                    count1 += 1
                else:
                    if(count1 > previous_count):
                        previous_count = count1
                    count1 = 0
            # final_count is used to store total number of times the small longest subsequence occurs
            final_count = 0
            count2 = 0
            for i in range(n):
                if(oct[i] != j):
                    count2 = 0
                else:
                    count2 += 1
                    if(count2 == previous_count):
                        final_count += 1
                        count2 = 0
            # print(previous_count, final_count)
            g2_.append(previous_count)
            g3_.append(final_count)

        # print(g2_,g3_)
        g2 = g2 + g2_
        g3 = g3 + g3_

        # 2d list to store entire small longest subsequence table
        g_final = []
        g_final.append(g0)
        g_final.append(g1)
        g_final.append(g2)
        g_final.append(g3)

        # print(df2.head())

        df_final = pd.DataFrame(g_final).transpose()
        # df_final = df_final.rename(columns=df_final.iloc[0], inplace = True)
        # print(df_final)

        df_final1 = pd.DataFrame(df_final.values[1:], columns=df_final.iloc[0])
        # print(df_final1)
        
        final = pd.concat([df2,df_final1], axis = 1)
        # print(final)
        
        final.to_excel('output_octant_longest_subsequence.xlsx', index = False)
    except:
        print("Error : File does not exist")

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

octant_longest_subsequence_count()
print("Code Compiled Successfully")