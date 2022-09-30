#Help https://youtu.be/H37f_x4wAC0
import os
os.system('cls')
import pandas as pd

def octant_longest_subsequence_count_with_range():
    try:
        df = pd.read_excel('input_octant_longest_subsequence_with_range.xlsx')
        # df = pd.read_excel('small_longest_subsequence_with_range.xlsx')
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
        

        final1 = pd.concat([df2,df_final_], axis = 1)
        # print(final.iloc[:,11:])

        final = new_df(n,time1,oct,l,g3_,final1)
        try:
            final.to_excel('output_octant_longest_subsequence_with_range.xlsx', index = False)
            print("Code Compiled Successfully")
        except:
            print("Error : It appears that output file has not be created")
    except:
        print("Error in calling function")

def new_df(n,time1,oct,l,g3_,semi__final):
    dk = []

    x = sum(g3_) + 18
    g0 = [" " for i in range(x)]
    g1 = [" ","Count"]
    l_ = ["+1","-1","+2","-2","+3","-3","+4","-4"]
    for i in range(len(l_)):
        g1.append(l_[i])
        g1.append("Time")
        gap = [" " for _ in range(g3_[i])]
        g1 = g1 + gap
    
    g2 = [" ","Longest Subsquence Length"]
    g3 = [" ","Count"]
    k0 = []
    k1 = []
    l_0 = []
    l_1 = []
    
    for j in l:
        count = 0
        prev = 0
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
        indexend = 0
        l0 = []
        l1 = []   
        for i in range(n):
            if(oct[i] != j):
                count1 = 0
            else:
                count1 += 1
            if(count1 == prev):
                c+=1
                count1 = 0
                indexend = i
                l0.append(indexend-prev+1)
                l1.append(indexend)
            #print(prev, c)
        l_0.append(l0)
        l_1.append(l1)
        k0.append(prev)
        k1.append(c)
    #print(l_0[0],type(l_1))
    #z = l_0[0]
    #print(z[0])
    for j in range(8):
        g2.append(k0[j])
        g2.append("From")
        z1 = l_0[j]
        for p in range(len(z1)):
            t = time1[z1[p]]
            g2.append(t)

    for j in range(8):
        g3.append(k1[j])
        g3.append("To")
        z2 = l_1[j]
        for p in range(len(z2)):
            t = time1[z2[p]]
            g3.append(t)
            
    #print(g3)

    dk.append(g0)
    dk.append(g1)
    dk.append(g2)
    dk.append(g3)
    d_f = pd.DataFrame(dk).transpose()
    df = pd.DataFrame(d_f.values[1:], columns=d_f.iloc[0])
    #print(semi__final,df)
    df_final = pd.concat([semi__final,df], axis = 1)
    return df_final


from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

octant_longest_subsequence_count_with_range()