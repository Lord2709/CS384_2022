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
        print(df2.head())
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