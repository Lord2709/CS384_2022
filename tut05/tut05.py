#Help https://youtu.be/N6PBd4XdnEw
import os
os.system('cls')
import openpyxl
import math
import numpy as np


def write_in_xlsx(range_of_rows,column_number,ls,ws):
    for i in range(1,range_of_rows+1):
        cellref=ws.cell(row=i, column=column_number)
        if i == 1:
            cellref.value = ls[0]
        else:
            cellref.value=ls[i-1]

def calculate_rank(vector):
    a={}
    rank=1
    for num in sorted(vector, reverse=True):
        if num not in a:
            a[num]=rank
            rank=rank+1
    return[a[i] for i in vector]
    
def octant_range_names(mod=5000):
    if os.path.exists("octant_output_ranking_excel.xlsx"):
        os.remove("octant_output_ranking_excel.xlsx")

    octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", "3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}
    
    wb = openpyxl.load_workbook('octant_input.xlsx')
    ws = wb['Sheet1']
    rows = ws.iter_rows(min_row = 0, max_row=29746, min_col = 1, max_col = 21)
    # print(rows)


    wb_output = openpyxl.Workbook()
    ws_output = wb_output.active
    mr = ws.max_row
    mc = ws.max_column
    for i in range (1, mr + 1):
        for j in range (1, mc + 1):
            c = ws.cell(row = i, column = j)
            ws_output.cell(row = i+1, column = j).value = c.value
    

    output = [[],[],[],[]]
    l_col = ['A','B','C','D']
    for i in range(4):
        col = ws_output[l_col[i]][2:]
        for cell in col:
            output[i].append(cell.value)
    # print(ws_output['A29747'].value)

    ws_output['E1'].value = " "
    ws_output['E2'].value = "U Avg"
    ws_output['E3'].value = np.mean(output[1])
    ws_output['F1'].value = " "
    ws_output['F2'].value = "V Avg"
    ws_output['F3'].value = np.mean(output[2])
    ws_output['G1'].value = " "
    ws_output['G2'].value = "W Avg"
    ws_output['G3'].value = np.mean(output[3])


    H = output[1] - ws_output['E3'].value
    I = output[2] - ws_output['F3'].value
    J = output[3] - ws_output['G3'].value
    H_col = [" ","U'=U-U Avg"]
    I_col = [" ","V'=V-V Avg"]
    J_col = [" ","W'=W-W Avg"]
    for i in range(len(H)):
        H_col.append(H[i])
        I_col.append(I[i])
        J_col.append(J[i])
    # print(H_col[29745])
    len_H = len(H_col)
    write_in_xlsx(len_H, 8, H_col, ws_output)
    write_in_xlsx(len_H, 9, I_col, ws_output)
    write_in_xlsx(len_H, 10, J_col, ws_output)

    Oct = [" ","Octant"]
    for i in range(len_H):
        if i==0 or i==1: 
            continue
        else:
            if((H_col[i]>=0) & (I_col[i]>=0) & (J_col[i]>=0)): Oct.append(1)
            if((H_col[i]>=0) & (I_col[i]>=0) & (J_col[i]<0)): Oct.append(-1)
            if((H_col[i]<0) & (I_col[i]>=0) & (J_col[i]>=0)): Oct.append(2)
            if((H_col[i]<0) & (I_col[i]>=0) & (J_col[i]<0)): Oct.append(-2)
            if((H_col[i]<0) & (I_col[i]<0) & (J_col[i]>=0)): Oct.append(3)
            if((H_col[i]<0) & (I_col[i]<0) & (J_col[i]<0)): Oct.append(-3)
            if((H_col[i]>=0) & (I_col[i]<0) & (J_col[i]>=0)): Oct.append(4)
            if((H_col[i]>=0) & (I_col[i]<0) & (J_col[i]<0)): Oct.append(-4)
    write_in_xlsx(len_H, 11, Oct, ws_output)

    L_col = ['','','','User Input']
    write_in_xlsx(len(L_col), 12, L_col, ws_output)

    M_col = ["", "Octant ID", "Overall Count",f"Mod {mod}"]

    n = 30000
    if n%mod == 0:
        n_ranges = n//mod
    else:
        n_ranges = math.ceil(n/mod)


    t = 0
    u = t + mod
    for j in range(n_ranges):
        if u <= 29745:
            if t==0:
                M_col.append(f"0000 - {u-1}")
            else:
                M_col.append(f"{t} - {u-1}")
        else:
            M_col.append(f"{t} - {len_H - 3}")
        t = u
        u += mod
    write_in_xlsx(len(M_col), 13, M_col, ws_output)

    # 8 new list are created to store the count value of {+1,-2,+2,-2,+3,-3,+4,-4}
    overall_count = []
    e = 0
    st = ["+1","-1","+2","-2","+3","-3","+4","-4"]
    for i in range(8):
        empty_list = [""]
        empty_list.append(st[e])
        overall_count.append(empty_list)
        e += 1

    df2 = Oct[2:]
    int_l = [1,-1,2,-2,3,-3,4,-4]
    j = 0
    for i in range(8):
        overall_count[i].append(df2.count(int_l[j]))
        overall_count[i].append(" ")
        j += 1
    # n --> given in tut01.pdf that max value will never exceed 30000.
    # Below while function is used to count the {+1,-2,+2,-2,+3,-3,+4,-4} values for different mod's

    N_col = ["","","","Octant ID"] + int_l
    O_col = ["","","","Octant Name","Internal outward interaction","External outward interaction",
            "External Ejection","Internal Ejection","External inward interaction",
            "Internal inward interaction","Internal sweep","External sweep"]

    k = 0
    m = mod
    n_r = n_ranges
    while n_r > 0:   
        n_r -= 1
        d_f = df2[k:m]
        j = 0
        for i in range(8):
            overall_count[i].append(d_f.count(int_l[j]))
            j += 1
        k = m 
        m = m + mod

    overall_count[0] += N_col
    overall_count[1] += O_col

    # print(overall_count)
    col = 14
    for i in range(8):
        if i == 2:
            col += 1
            continue
        write_in_xlsx(len(overall_count[i]), col, overall_count[i], ws_output)
        col += 1

    wb_output.save("octant_output_ranking_excel.xlsx")

    #Rank
    overall_rank = [[1,"Rank of 1"],[-1,"Rank of 2"],[2,"Rank of 3"],[-2,"Rank of 4"],[3,"Rank of 5"],[-3,"Rank of 6"],[4,"Rank of 7"],[-4,"Rank of 8"]]

    row_list = []
    imp_element_pos = [2] + [i for i in range(4,n_ranges+4)]
    for i in imp_element_pos:
        l = []
        for j in range(8):
            l.append(overall_count[j][i])
        row_list.append(l)


    rank_list = []
    for i in range(len(row_list)):
        rank_list.append(calculate_rank(row_list[i]))

    for i in range(len(overall_rank)):
        for j in rank_list:
            overall_rank[i].append(j[i])
        overall_rank[i].insert(3,"")
        # print(overall_rank[1])

    col = 22
    for i in range(8):
        write_in_xlsx(len(overall_rank[i]), col, overall_rank[i], ws_output)
        col += 1
    
    wb_output.save("octant_output_ranking_excel.xlsx")

###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod=5000 
octant_range_names(mod)

