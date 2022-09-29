#Help https://youtu.be/H37f_x4wAC0
import os
os.system('cls')
import pandas as pd

def octant_longest_subsequence_count():
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


from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count()