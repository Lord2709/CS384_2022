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

        # df1 variable stores the data frame which contains ua, va, wa values
        # df2 variable stores the main data frame after concatenating df and df1
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

        # An 2D List (overall_count) is created to store the entire columns representing values --> {+1,-2,+2,-2,+3,-3,+4,-4}
        overall_count = []
        e = 0
        # st list is used to append string values in 2D list and also to loop through it ahead in the code
        st = ["+1","-1","+2","-2","+3","-3","+4","-4"] 
        for i in range(8):
            # empty_list will store values of each column represented by the values --> {+1,-2,+2,-2,+3,-3,+4,-4}
            empty_list = []
            empty_list.append(st[e])
            overall_count.append(empty_list) # Column appended in overall_count 2D list
            e += 1

        int_l = [1,-1,2,-2,3,-3,4,-4]
        j = 0
        for i in range(8):
            overall_count[i].append((df2['Octant'] == int_l[j]).value_counts()[1])
            overall_count[i].append(" ")
            j += 1

        # n --> given in tut02.pdf that max value will never exceed 30000.
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
            j = 0
            for i in range(8):
                overall_count[i].append((d_f['Octant'] == int_l[j]).value_counts()[1])
                j += 1
            k = m 
            m = m + mod

        # Below 'for' loop used to append 'Verified' row to the overall_count list
        j = 0
        for i in range(8):
            #print(type(i))
            overall_count[i].append((df2['Octant'] == int_l[j]).value_counts()[1])
            j += 1

        c_0 = [" ", " ","User Input"]
        for i in range(n_ranges):
            c_0.append(" ")
        
        # This particular part of code is used to mention the ranges of mod in the column
        c0 = ["Octant ID", "Overall Count"]
        c0.append(f"Mod {mod}")
        t = 0
        u = t + mod
        for j in range(n_ranges+1):
            if u <= len(df2["Octant"]):
                if t==0:
                    c0.append(f"{0000} - {u-1}")
                else:
                    c0.append(f"{t} - {u-1}")
            elif j == n_ranges:
                c0.append("Verified")
            else:
                c0.append(f"{t} - {df2.shape[0] - 1}")
            t = u
            u += mod
    
    # final_count 2D list stores all the columns ahead of 'Octant' column
        final_count = []
        final_count.append(c_0)
        final_count.append(c0)
        for i in range(8):
            final_count.append(overall_count[i])

        # transpose is used to convert list into columns of the 2D list
        df_final = pd.DataFrame(final_count).transpose()
        #print(df_final)

        df_final_ = pd.DataFrame(df_final.values[1:], columns=df_final.iloc[0])
        #print(df_final_)
        
        col = df_final_.columns
        #print(df_final_)
        
        oct0 = df2['Octant'].to_list() 

        q = 0
        r = mod

        df_final_ = gap(df_final_, col, 0, oct0, mod, q, r)
        df_final_ = gap(df_final_, col, 1, oct0, mod, q, r)
        
        while n_ranges > 0:   
            n_ranges -= 1
            d_f = df2.iloc[q:r]
            df_final_ = gap(df_final_,col,2,oct0,mod,q,r)
            df_final_ = gap(df_final_,col,3,oct0,mod,q,r)
            q = r 
            r = r + mod
        
        final = pd.concat([df2,df_final_], axis = 1)
        #print(final.iloc[:,11:])
        try:
            final.to_excel('output_octant_transition_identify.xlsx',index = False)
            print("Code Compiled Successfully")
        except:
            print("Error : It seems that no output file has been generated.")
    except:
        print("Error in calling function")
        exit()

# gap function is created to append gaps betwwen 2 tables and also to calculate overall & mod transition count
def gap(d,col,k,oct,mod,q,r):
    try:
        g_df = []
        # g_df is the overall 2D list which will be created everytime gap function is called
        if k==0 or k==2:
            g0 = [" " for i in range(5)]
            if k==0:
                g1 = [" "," "," ","Overall Transition Count"," "]
            else:
                if r <= len(oct):
                    if q==0:
                        p = f"{0000} - {r-1}"
                    else:
                        p = f"{q} - {r-1}"
                else:
                    p = f"{q} - {len(oct) - 1}"
                g1 = [" "," "," ","Mod Transition Count"]
                g1.append(p)
            g2 = [" "," "," "," ","To"]
            g_df.append(g0)
            g_df.append(g1)
            g_df.append(g2)
            for i in range(7):
                g_df.append(g0)
        elif k==1 or k==3:
            g0_ = [" "," ","From"] + [" " for i in range(8)]
            g0 = [" ","Count","+1","-1","+2","-2","+3","-3","+4","-4"] 
            lg = [1,-1,2,-2,3,-3,4,-4]
            st = ["+1","-1","+2","-2","+3","-3","+4","-4"] 
            g_df.append(g0_)
            g_df.append(g0)
            
            for j in range(8):
                l0 = [" "]
                x = st[j]
                l0.append(x)
                l1 = [0]*8

                if k==1:
                    d__f = oct
                else:
                    d__f = oct[q:r+1]
                for i in range(2,len(d__f)+1):  
                    if(d__f[i-1] == lg[j]):
                        if(d__f[i-2] == 1):
                            l1[0] += 1
                        elif(d__f[i-2] == -1):
                            l1[1] += 1
                        elif(d__f[i-2] == 2):
                            l1[2] += 1
                        elif(d__f[i-2] == -2):
                            l1[3] += 1
                        elif(d__f[i-2] == 3):
                            l1[4] += 1
                        elif(d__f[i-2] == -3):
                            l1[5] += 1
                        elif(d__f[i-2] == 4):
                            l1[6] += 1
                        elif(d__f[i-2] == -4):
                            l1[7] += 1 
                #print(l0,type(lg))
                lf = l0 + l1
                g_df.append(lf)
        g_df_final = pd.DataFrame(g_df).transpose()
        g_df_final_ = pd.DataFrame(g_df_final.values[1:], columns=col)
        #print(g_df_final_)
        # gap between table or the data table as a dataframe is appended to the main dataframe(d)
        x = pd.concat([d,g_df_final_],ignore_index = True)
        return x
    except:
        print("Invalid argument was passed to the Gap Function")

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod=5000
octant_transition_count(mod)