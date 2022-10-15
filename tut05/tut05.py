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

