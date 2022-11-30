#https://youtu.be/0srus9mXEhk
# Libraries...
import os
os.system('cls')
import ntpath
import glob
import pandas as pd
import numpy as np
import datetime
from pathlib import Path 
from datetime import datetime 
import streamlit as st
import re
import time
from PIL import Image
from zipfile import ZipFile
from os.path import basename


start_time = datetime.now() 
print(start_time.strftime("%c"))


# global variables...
global data
global index
index = 0
global g
g = 9.81
global k
global Lambda
# ====================


def proj_psat_gui():
    col1, col2, col3 = st.columns(3)
    col2.header("PROJECT 3")

    try:
        image = Image.open("proj3_img.jpg")
    except:
        print("Error in opening image.")

    st.image(image)

    global k
    global Lambda
    global name

    try:
        fileList = open('input_file_list.txt', 'r')
        files = fileList.readlines()
    except:
        print("Error in opening input_file_list.")


    for file in files:
        input_filename = file.strip()
        
        base = (Path(input_filename).stem.strip())
        output_csv = base+".csv"
        
        header_list = ['Time','SL' ,'counter' ,'U','V','W','W1','AMP-U' ,'AMP-V' ,'AMP-W' ,'AMP-W1' ,'SNR_U','SNR_V','SNR_W','SNR-W1' ,'Corr_U','Corr_V','Corr_W','Corr-W1']
        
        try:
            dataframe = pd.read_csv(input_filename,delimiter=" +")
        except:
            print("Error in reading csv file using pandas.")
        try:
            dataframe.to_csv(output_csv, encoding='utf-8', header=header_list, index=False)
        except:
            print("Not able to convert dataframe to csv using pandas.")

    index=0
    # corr= 70
    # SNR= 15 
    # Lambda=1.5
    # k=1.5
    g=9.81
    # N=input_data['U'].count()


    # Adding Column Headings...
    try:
        with open(r"Results_v2.csv",mode='a') as file_:
            file_.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(start_time.strftime("%c"),"average_velocity_U","average_velocity_V","average_velocity_W","U_variance_Prime","V_variance_Prime","W_variance_Prime","U_stdev_Prime","V_stdev_Prime","W_stdev_Prime","Skewness_U_Prime","Skewness_V_Prime","Skewness_W_Prime","Kurtosis_U_Prime","Kurtosis_V_Prime","Kurtosis_W_Prime","Reynolds_stress_u\'v\'","Reynolds_stress_u\'w\'","Reynolds_stress_v\'w\'","Anisotropy","M30","M03","M12","M21","fku_2d","Fku_2d","fkw_2d","Fkw_2d","fku_3d","Fku_3d","fkw_3d","Fkw_3d","TKE_3d","Q1_K_Value","Q2_K_Value","Q3_K_Value","Q4_K_Value","e","ED","Octant_plus_1","Octant_minus_1","Octant_plus_2","Octant_minus_2","Octant_plus_3","Octant_minus_3","Octant_plus_4","Octant_minus_4","Total_Octant_sample","Probability_Octant_plus_1","Probability_Octant_minus_1","Probability_Octant_plus_2","Probability_Octant_minus_2","Probability_Octant_plus_3","Probability_Octant_minus_3","Probability_Octant_plus_4","Probability_Octant_minus_4","Min_Octant_Count","Min_Octant_Count_id","Max_Octant_Count","Max_Octant_Count_id","\n"))
    except:
        print("Error in opening Results_v2.csv file")


    # User Innputs ======================================================================
    constant_fk2d = st.text_input("Enter constant_fk2d \"numeric\" value: ")
    if bool(re.search('[a-z]', constant_fk2d, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', constant_fk2d)):
        st.warning('Entered value contains alphabets/special characters...    \"Re-Enter constant_fk2d value!\"', icon="⚠️")

    multiplying_factor_3d = st.text_input("Enter Multiplying Factor value: ")
    if bool(re.search('[a-z]', multiplying_factor_3d, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', multiplying_factor_3d)):
        st.warning('Entered value contains alphabets/special characters...    \"Re-Enter Multiplying Factor value!\"', icon="⚠️")

    Shear_velocity = st.text_input("Enter Shear Velocity value: ")
    if bool(re.search('[a-z]', Shear_velocity, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', Shear_velocity)):
        st.warning('Entered value contains alphabets/special characters...    \"Re-Enter Shear Velocity value!\"', icon="⚠️")
    # ====================================================================================

    # Using regex to prevent unwanted input from user to cause any error ahead in the program.
    if bool(re.search('[.]', constant_fk2d)):
        if constant_fk2d.rsplit(".")[len(constant_fk2d.rsplit("."))-1] == '0':
            constant_fk2d = int(float(constant_fk2d))
        elif bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', constant_fk2d)):
            pass
        else:
            constant_fk2d = float(constant_fk2d)


    if bool(re.search('[.]', multiplying_factor_3d)):
        if multiplying_factor_3d.rsplit(".")[len(multiplying_factor_3d.rsplit("."))-1] == '0':
            multiplying_factor_3d = int(float(multiplying_factor_3d))
        elif bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', multiplying_factor_3d)):
            pass
        else:
            multiplying_factor_3d = float(multiplying_factor_3d)


    if bool(re.search('[.]', Shear_velocity)):
        if Shear_velocity.rsplit(".")[len(Shear_velocity.rsplit("."))-1] == '0':
            Shear_velocity = int(float(Shear_velocity))
        elif bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', Shear_velocity)):
            pass
        else:
            Shear_velocity = float(Shear_velocity)

    # =========================================================================================

    st.subheader("Filtering Methods listed below...")

    # Displaying Filtering Option on streamlit platform
    col1, col2, col3 = st.columns(3)
    tch_text = ['1. C','2. S','3. A','4. C & S','5. C & A','6. S & A','7. C & S & A','8. all combine']
    for x in tch_text:
        col2.write(x)

    # user input
    tch = st.text_input("Chose Filtering Method From Above: ")

    # Using regex to prevent unwanted input from user to cause any error ahead in the program.
    if bool(re.search('[a-z 09]', tch, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|.}{~:.]', tch)):
        st.warning('Enter Option Number alloted to the provided Filtering Method only..."', icon="⚠️")
    else:
        if len(list(map(int,tch.split()))) == 0:
            pass
        else:
            tch = list(map(int,tch.split()))[0]
            # print(tch, type(tch))
        
        
    filter = False
    
    if tch == 1:
        col1, col2, col3 = st.columns(3)
        corr = col2.text_input("Enter Threshold Value C: ")
        if bool(re.search('[a-z]', corr, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', corr)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value C!\"', icon="⚠️")
        else:
            if len(list(map(int,corr.split()))) == 0:
                pass
            else:
                corr = list(map(int,corr.split()))[0]
                filter = True

    elif tch == 2:

        col1, col2, col3 = st.columns(3)
        SNR = col2.text_input("Enter Threshold Value S: ")
        if bool(re.search('[a-z]', SNR, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', SNR)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value S!\"', icon="⚠️")
        else:
            if len(list(map(int,SNR.split()))) == 0:
                pass
            else:
                SNR = list(map(int,SNR.split()))[0]
                filter = True

    elif tch == 3:
        count = 0

        col1, col2, col3 = st.columns(3)
        Lambda = col2.text_input("Enter Lambda Value for A: ")
        if bool(re.search('[a-z]', Lambda, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', Lambda)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter Lambda Value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', Lambda)):
                Lambda = float(Lambda)
                count += 1


        col1, col2, col3 = st.columns(3)
        k = col2.text_input("Enter k value for A: ")
        if bool(re.search('[a-z]', k, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', k)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter k value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', k)):
                k = float(k)
                count += 1

        if count == 2:
            filter = True
       
    elif tch == 4:
        count = 0

        col1, col2, col3 = st.columns(3)
        corr = col2.text_input("Enter Threshold Value C: ")
        if bool(re.search('[a-z]', corr, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', corr)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value C!\"', icon="⚠️")
        else:
            if len(list(map(int,corr.split()))) == 0:
                pass
            else:
                corr = list(map(int,corr.split()))[0]
                count += 1

        
        col1, col2, col3 = st.columns(3)
        SNR = col2.text_input("Enter Threshold Value S: ")
        if bool(re.search('[a-z]', SNR, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', SNR)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value S!\"', icon="⚠️")
        else:
            if len(list(map(int,SNR.split()))) == 0:
                pass
            else:
                SNR = list(map(int,SNR.split()))[0]
                count += 1

        if count == 2:
            filter = True

    elif tch == 5:
        count = 0

        col1, col2, col3 = st.columns(3)
        corr = col2.text_input("Enter Threshold Value C: ")
        if bool(re.search('[a-z]', corr, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', corr)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value C!\"', icon="⚠️")
        else:
            if len(list(map(int,corr.split()))) == 0:
                pass
            else:
                corr = list(map(int,corr.split()))[0]
                count += 1

        col1, col2, col3 = st.columns(3)
        Lambda = col2.text_input("Enter Lambda Value for A: ")
        if bool(re.search('[a-z]', Lambda, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', Lambda)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter Lambda Value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', Lambda)):
                Lambda = float(Lambda)
                count += 1


        col1, col2, col3 = st.columns(3)
        k = col2.text_input("Enter k value for A: ")
        if bool(re.search('[a-z]', k, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', k)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter k value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', k)):
                k = float(k)
                count += 1

        if count == 3:
            filter = True

    elif tch == 6:
        count = 0

        col1, col2, col3 = st.columns(3)
        SNR = col2.text_input("Enter Threshold Value S: ")
        if bool(re.search('[a-z]', SNR, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', SNR)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value S!\"', icon="⚠️")
        else:
            if len(list(map(int,SNR.split()))) == 0:
                pass
            else:
                SNR = list(map(int,SNR.split()))[0]
                count += 1

        
        col1, col2, col3 = st.columns(3)
        Lambda = col2.text_input("Enter Lambda Value for A: ")
        if bool(re.search('[a-z]', Lambda, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', Lambda)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter Lambda Value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', Lambda)):
                Lambda = float(Lambda)
                count += 1


        col1, col2, col3 = st.columns(3)
        k = col2.text_input("Enter k value for A: ")
        if bool(re.search('[a-z]', k, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', k)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter k value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', k)):
                k = float(k)
                count += 1

        if count == 3:
            filter = True

    elif tch == 7 or tch==8:
        count = 0

        col1, col2, col3 = st.columns(3)
        corr = col2.text_input("Enter Threshold Value C: ")
        if bool(re.search('[a-z]', corr, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', corr)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value C!\"', icon="⚠️")
        else:
            if len(list(map(int,corr.split()))) == 0:
                pass
            else:
                corr = list(map(int,corr.split()))[0]
                count += 1

        
        col1, col2, col3 = st.columns(3)
        SNR = col2.text_input("Enter Threshold Value S: ")
        if bool(re.search('[a-z]', SNR, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:.]', SNR)):
            st.warning('Entered value contains alphabets/special characters/float ...    \"Re-Enter Threshold Value S!\"', icon="⚠️")
        else:
            if len(list(map(int,SNR.split()))) == 0:
                pass
            else:
                SNR = list(map(int,SNR.split()))[0]
                count += 1


        col1, col2, col3 = st.columns(3)
        Lambda = col2.text_input("Enter Lambda Value for A: ")
        if bool(re.search('[a-z]', Lambda, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', Lambda)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter Lambda Value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', Lambda)):
                Lambda = float(Lambda)
                count += 1


        col1, col2, col3 = st.columns(3)
        k = col2.text_input("Enter k value for A: ")
        if bool(re.search('[a-z]', k, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|}{~:]', k)):
            st.warning('Entered value contains alphabets/special characters ...    \"Re-Enter k value for A!\"', icon="⚠️")
        else:
            if bool(re.search('[.]', k)):
                k = float(k)
                count += 1

        if count==4:
            filter = True



    # if "filter" value is True, then only "sch" value will be accepted.
    if filter:
        st.subheader("Replacement Methods listed below...")

        col1, col2, col3 = st.columns(3)
        sch_text = ['1. previous point','2. 2*last-2nd_last','3. overall_mean', '4. 12_point_strategy','5. mean of previous 2 point', '6. all seqential','7. all parallel']
        for x in sch_text:
            col2.write(x)


        sch = st.text_input("Chose Filtering Method From Above: ", key = 1000)

        if bool(re.search('[a-z 089]', sch, re.IGNORECASE)) or bool(re.search('[@_!#$%^&*()<>?/\|.}{~:.]', sch)):
            st.warning('Enter Option Number alloted to the provided Filtering Method only..."', icon="⚠️")
        else:
            if len(list(map(int,sch.split()))) == 0:
                time.sleep(15)
                pass
            else:
                sch = list(map(int,sch.split()))[0]


        
        global data
        fileList = open('input_file_list.txt', 'r')
        files = fileList.readlines()
        for file in files:
            input_filename=file.strip()[:-3]+'csv'
            try:
                input_data = pd.read_csv(input_filename)
            except:
                print(input_filename)
                continue
            N=input_data['U'].count()
            
            if tch==1 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_All(i,corr,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
                    
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_One(i,corr,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
        
            if tch==2 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    SNR_All(i,SNR,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_SNR{SNR}_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)    
                    name = add_front_name(name,i)
                    store()
                
                    data =input_data
                    find_mean()
                    find_std()
                    SNR_One(i,SNR,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_SNR{SNR}_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
        
            if tch==3 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_acceleration_1.5_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
            
                    data =input_data
                    find_mean()
                    find_std()
                    update_acceleration_one_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_acceleration_1.5_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
        
            if tch==4 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_All(i,corr,N)
                    SNR_All(i,SNR,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_SNR{SNR}_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
                    
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_One(i,corr,N)
                    SNR_One(i,SNR,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_SNR{SNR}_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
        
            if tch==5 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    SNR_All(i,SNR,N)
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_SNR{SNR}_Acceleration_1.5_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
                
                    data =input_data
                    find_mean()
                    find_std()
                    SNR_One(i,SNR,N)
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_SNR{SNR}_acceleration_1.5_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
        
            if tch==6 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_All(i,corr,N)
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_Acceleration_1.5_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
                
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_One(i,corr,N)
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_acceleration_1.5_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    name = add_front_name(name,i)
                    store()
        
            if tch==7 or tch==8:
                if sch>5:
                    iList = [1,2,3,4,5]
                else:
                    iList = [sch]
                for i in iList:
                    if sch==7:
                        input_data = pd.read_csv(input_filename)
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_All(i,corr,N)
                    SNR_All(i,SNR,N)
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_SNR{SNR}_Acceleration_1.5_all_replacement_strategy_{i}"
                    write_timestamp_to_file(name)
                    
                    name = add_front_name(name,i)
                    store()
                
                    data =input_data
                    find_mean()
                    find_std()
                    Corr_One(i,corr,N)
                    SNR_One(i,SNR,N)
                    update_acceleration_all_at_time(i,N)
                    allfunction(N)
                    name = f"{input_filename}_filtered_by_correlation{corr}_SNR{SNR}_acceleration_1.5_individual_replacement_strategy_{i}"
                    write_timestamp_to_file(name)    
                    name = add_front_name(name,i)
                    store()

        st.success("Successfully Updated Output Files.")
      
        # create a ZipFile object
        dirName = os.getcwd().replace("\\","/")

        with ZipFile('Results_v2.zip', 'w') as zipObj:
        # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(dirName):
                for filename in filenames:
                    if filename == "Results_v2.csv":
                        #create complete filepath of file in directory
                        filePath = os.path.join(folderName, filename)
                        # Add file to zip
                        zipObj.write(filePath, basename(filePath))

        col1, col2, col3 = st.columns(3)
        with open("Results_v2.zip", "rb") as fp:
            btn = col2.download_button(
                label="Download Result File",
                data=fp,
                file_name="Results_v2.zip",
                mime="application/zip"
            )



try:
    def write_timestamp_to_file(name): 
        # creating the csv writer 
        # storing current date and time
        current_date_time = datetime.now()
        print("\nCurrent System Time: ", current_date_time)
        file1 = open("methods_timestamp.csv", "a")  # append mode
        file1.write(name + ","+ str(current_date_time)+"\n")
        file1.close()
except:
    print("Error in calling write_timestamp_to_file function")


try:
    def duration_timestamp_to_file(name, duration):  
        file1 = open("methods_timestamp.csv", "a")  # append mode
        file1.write(name +   ","+str(duration)+"\n")
        file1.close()
except:
    print("Error in calling duration_timestamp_to_file function")

try:
    def useful_values_u():
        data['Var_u\'']=data['std_u\'']=data['Skewness_u\'']=data['Kurtosis_u\'']=''

        data['u\'u\'']=round(data['u\'']**2,3)
        data.at[0,'Var_u\'']=round(data['u\'u\''].mean(),3) #variance
        u_std=round(data['u\''].std(),3)
        data.at[0,'std_u\'']=u_std                          #standard deviation
        data.at[0,'Skewness_u\'']=round(data['u\''].skew(),3)#skewness
        data.at[0,'Kurtosis_u\'']=round(data['u\''].kurt(),3)#kurtosis
        data['u^']=round(data['u\'']/u_std,3)
except:
    print("Error in calling useful_values_u function")


try:
    def useful_values_v():
        data['Var_v\'']=data['std_v\'']=data['Skewness_v\'']=data['Kurtosis_v\'']=''

        data['v\'v\'']=round(data['v\'']**2,3)
        data.at[0,'Var_v\'']=round(data['v\'v\''].mean(),3) #variance
        u_std=round(data['v\''].std(),3)
        data.at[0,'std_v\'']=u_std                          #standard deviation
        data.at[0,'Skewness_v\'']=round(data['v\''].skew(),3)#skewness
        data.at[0,'Kurtosis_v\'']=round(data['v\''].kurt(),3)#kurtosis
        data['v^']=round(data['v\'']/u_std,3)
except:
    print("Error in calling useful_values_v function")    

try:
    def useful_values_w():
        data['Var_w\'']=data['std_w\'']=data['Skewness_w\'']=data['Kurtosis_w\'']=''

        data['w\'w\'']=round(data['w\'']**2,3)
        data.at[0,'Var_w\'']=round(data['w\'w\''].mean(),3) #variance
        w_std=round(data['w\''].std(),3)
        data.at[0,'std_w\'']=w_std                           #standard deviation
        data.at[0,'Skewness_w\'']=round(data['w\''].skew(),3)#skewness
        data.at[0,'Kurtosis_w\'']=round(data['w\''].kurt(),3)#kurtosis
        data['w^']=round(data['w\'']/w_std,3)
except:
    print("Error in calling useful_values_w function")


try:
    def useful_values():

        data['U_mean']=data['V_mean']=data['W_mean']=''
        U_mean=round(data['U'].mean(),3)
        V_mean=round(data['V'].mean(),3)
        W_mean=round(data['W'].mean(),3)

        data.at[index,'U_mean']=U_mean
        data.at[index,'V_mean']=V_mean
        data.at[index,'W_mean']=W_mean

        data['u\'']=round(data['U']-U_mean,3)
        data['v\'']=round(data['V']-V_mean,3)
        data['w\'']=round(data['W']-W_mean,3)

        N=data['U'].count()
        
        useful_values_u()
        useful_values_v()
        useful_values_w()
            
        data['Reynolds_stress_u\'v\'']=data['Reynolds_stress_u\'w\'']=data['Reynolds_stress_v\'w\'']=''
        
        data['u\'v\'']=data['u\'']*data['v\'']
        data.at[0,'Reynolds_stress_u\'v\'']=round(data['u\'v\''].mean(),3)
        
        data['u\'w\'']=data['u\'']*data['w\'']
        data.at[0,'Reynolds_stress_u\'w\'']=round(data['u\'w\''].mean(),3)
        
        data['v\'w\'']=data['v\'']*data['w\'']
        data.at[0,'Reynolds_stress_v\'w\'']=round(data['v\'w\''].mean(),3)
        
        data.at[0,'anisotropy']=round(data.at[0,'std_w\'']/data.at[0,'std_u\''],3)
        data['M30']=data['M03']=data['M12']=data['M21']=''

        data['u^u^w^']=round((data['u^']**2)*(data['w^']),3)
        data['u^w^w^']=round((data['w^']**2)*(data['u^']),3)
        data['u^u^u^']=round(data['u^']**3,3)
        data['w^w^w^']=round(data['w^']**3,3)
        
        data.at[0,'M21']=round(data['u^u^w^'].mean(),3)
        data.at[0,'M12']=round(data['u^w^w^'].mean(),3)
        data.at[0,'M30']=round(data['u^u^u^'].mean(),3)
        data.at[0,'M03']=round(data['w^w^w^'].mean(),3)
except:
    print("Error in calling useful_values function")


try:
    def fk():
        data['fku_2d']=data['Fku_2d']=data['fkw_2d']=data['Fkw_2d']=''
        data['u\'u\'u\'']=round(data['u\'']**3,3)
        data['u\'u\'u\' mean']=''
        data.at[0,'u\'u\'u\' mean']=round(data['u\'u\'u\''].mean(),3)

        data['u\'w\'w\'']=round((data['w\'']**2)*(data['u\'']),3)
        data['u\'w\'w\' mean']=''
        data.at[0,'u\'w\'w\' mean']=round(data['u\'w\'w\''].mean(),3)

        data['w\'w\'w\'']=round(data['w\'']**3,3)
        data['w\'w\'w\' mean']=''
        data.at[0,'w\'w\'w\' mean']=round(data['w\'w\'w\''].mean(),3)

        data['w\'u\'u\'']=round((data['u\'']**2)*(data['w\'']),3)
        data['w\'u\'u\' mean']=''
        data.at[0,'w\'u\'u\' mean']=round(data['w\'u\'u\''].mean(),3)

        data['u\'v\'v\'']=round((data['v\'']**2)*(data['u\'']),3)
        data['u\'v\'v\' mean']=''
        data.at[0,'u\'v\'v\' mean']=round(data['u\'v\'v\''].mean(),3)

        data['w\'v\'v\'']=round((data['v\'']**2)*(data['w\'']),3)
        data['w\'v\'v\' mean']=''
        data.at[0,'w\'v\'v\' mean']=round(data['w\'v\'v\''].mean(),3)

        constant_fk2d=0.75 
        multiplying_factor_3d=0.5 
        Shear_velocity=2.6**3

        data.at[index,'fku_2d']=round((data.at[0,'u\'u\'u\' mean']+data.at[0,'u\'w\'w\' mean'])*constant_fk2d,3)
        data.at[index,'Fku_2d']=round(data.at[index,'fku_2d']/Shear_velocity,3)

        data.at[index,'fkw_2d']=round((data.at[0,'w\'w\'w\' mean']+data.at[0,'w\'u\'u\' mean'])*constant_fk2d,3)
        data.at[index,'Fkw_2d']=round(data.at[index,'fkw_2d']/Shear_velocity,3)

        data['fku_3d']=data['Fku_3d']=data['fkw_3d']=data['Fkw_3d']=data['TKE_3d']=''

        data.at[index,'fku_3d']=round((data.at[0,'u\'u\'u\' mean']+ data.at[0,'u\'w\'w\' mean'] + data.at[0,'u\'v\'v\' mean'] )*multiplying_factor_3d,3)
        data.at[index,'Fku_3d']=round(data.at[index,'fku_2d']/Shear_velocity,3)

        data.at[index,'fkw_3d']=round((data.at[0,'w\'w\'w\' mean']+data.at[0,'w\'u\'u\' mean'] + data.at[0,'w\'v\'v\' mean'])*multiplying_factor_3d,3)
        data.at[index,'Fkw_3d']=round(data.at[index,'fkw_3d']/Shear_velocity,3)

        data.at[index,'TKE_3D']=round((data.at[0,'Var_v\'']*data.at[0,'Var_u\'']*data.at[0,'Var_w\''])* multiplying_factor_3d,3)
except:
    print("Error in calling fk function")


try:
    def Q_K_Value():
        data['Q1_K_Value']=data['Q2_K_Value']=data['Q3_K_Value']=data['Q4_K_Value']=''
        u_std=round(data['u\''].std(),3)
        w_std=round(data['w\''].std(),3)
        value=u_std*w_std
        X=10000
        k_first=k_second=k_third=k_fourth=0
        first=[0]*X
        second=[0]*X
        third=[0]*X
        fourth=[0]*X
        
        
        for i,row in data.iterrows():
            x=data.at[i,'u\'']*data.at[i,'w\'']
            if x<0:
                x=x*-1
                
            y=x/value
            z=int(y)
            if data.at[i,'u\'']>0 and data.at[i,'w\'']>0:
                first[z]=1
            if data.at[i,'u\'']<0 and data.at[i,'w\'']>0:
                second[z]=1
            if data.at[i,'u\'']<0 and data.at[i,'w\'']<0:
                third[z]=1
            if data.at[i,'u\'']>0 and data.at[i,'w\'']<0:
                fourth[z]=1
                
        for i in range(X):
            if first[X-i-1]!=0:
                data.at[index,'Q1_K_Value']=X-i
                break
                
        for i in range(X):
            if second[X-i-1]!=0:
                data.at[index,'Q2_K_Value']=X-i
                break
                
        for i in range(X):
            if third[X-i-1]!=0:
                data.at[index,'Q3_K_Value']=X-i
                break
                
        for i in range(X):
            if fourth[X-i-1]!=0:
                data.at[index,'Q4_K_Value']=X-i
                break
except:
    print("Error in calling Q_K_Value function")


try:
    def octant_ID(N):
        data['Octant_id']=0
        for i in range(N):
            if data.at[i,'u\'']>=0 and data.at[i,'v\'']>=0:
                if data.at[i,'w\'']>=0:
                    data.at[i,'Octant_id']=1
                if data.at[i,'w\'']<0:
                    data.at[i,'Octant_id']=-1

            if data.at[i,'u\'']<0 and data.at[i,'v\'']>=0:
                if data.at[i,'w\'']>=0:
                    data.at[i,'Octant_id']=2
                if data.at[i,'w\'']<0:
                    data.at[i,'Octant_id']=-2

            if data.at[i,'u\'']<0 and data.at[i,'v\'']<0:
                if data.at[i,'w\'']>=0:
                    data.at[i,'Octant_id']=3
                if data.at[i,'w\'']<0:
                    data.at[i,'Octant_id']=-3

            if data.at[i,'u\'']>=0 and data.at[i,'v\'']<0:
                if data.at[i,'w\'']>=0:
                    data.at[i,'Octant_id']=4
                if data.at[i,'w\'']<0:
                    data.at[i,'Octant_id']=-4
except:
    print("Error in calling octant_ID function")


try:
    def octant_column(N):
        data['Octant_plus_1']=data['Octant_minus_1']=''
        data['Octant_plus_2']=data['Octant_minus_2']=''
        data['Octant_plus_3']=data['Octant_minus_3']=''
        data['Octant_plus_4']=data['Octant_minus_4']=''
        data['Total_Octant_sample']=''

        data['Probability_Octant_plus_1']=data['Probability_Octant_minus_1']=''
        data['Probability_Octant_plus_2']=data['Probability_Octant_minus_2']=''
        data['Probability_Octant_plus_3']=data['Probability_Octant_minus_3']=''
        data['Probability_Octant_plus_4']=data['Probability_Octant_minus_4']=''

        data['Min_Octant_Count']=data['Min_Octant_Count_id']=''
        data['Max_Octant_Count']=data['Max_Octant_Count_id']=''

        data.at[index,'Min_Octant_Count']=data.at[index,'Min_Octant_Count_id']=N
        data.at[index,'Max_Octant_Count']=data.at[index,'Max_Octant_Count_id']=0

except:
    print("Error in calling octant_column function")


try:
    def max_min_update(i,j):
        if(data.at[index,'Min_Octant_Count']>i):
            data.at[index,'Min_Octant_Count']=i
            data.at[index,'Min_Octant_Count_id']=j
        if(data.at[index,'Max_Octant_Count']<i):
            data.at[index,'Max_Octant_Count']=i
            data.at[index,'Max_Octant_Count_id']=j
except:
    print("Error in calling max_min_update function")


try:
    def octant(N):
        octant_ID(N)
        octant_column(N)
        
        # add all octant value with 4 to make it positive to store data in array
        # {-4,0},{-3,1},{-2,2},{-1,3},{NaN,4},{1,5},{2,6},{3,7},{4,8}
        octant_values_frequency=[0]*9 #array of size 9
        for i in range(N):
            x=data.at[i,'Octant_id']
            octant_values_frequency[x+4]+=1

        
        #for id 1
        data.at[index,'Octant_plus_1']=octant_values_frequency[1+4]
        data.at[index,'Probability_Octant_plus_1']=round(octant_values_frequency[1+4]/N,3)
        max_min_update(octant_values_frequency[1+4],1)

        #for id -1
        data.at[index,'Octant_minus_1']=octant_values_frequency[-1+4]
        data.at[index,'Probability_Octant_minus_1']=round(octant_values_frequency[-1+4]/N,3)
        max_min_update(octant_values_frequency[-1+4],-1)

        #for id 2
        data.at[index,'Octant_plus_2']=octant_values_frequency[2+4]
        data.at[index,'Probability_Octant_plus_2']=round(octant_values_frequency[2+4]/N,3)
        max_min_update(octant_values_frequency[2+4],2)

        #for id -2
        data.at[index,'Octant_minus_2']=octant_values_frequency[-2+4]
        data.at[index,'Probability_Octant_minus_2']=round(octant_values_frequency[-2+4]/N,3)
        max_min_update(octant_values_frequency[-2+4],-2)

        #for id 3
        data.at[index,'Octant_plus_3']=octant_values_frequency[3+4]
        data.at[index,'Probability_Octant_plus_3']=round(octant_values_frequency[3+4]/N,3)
        max_min_update(octant_values_frequency[3+4],3)

        #for id -3
        data.at[index,'Octant_minus_3']=octant_values_frequency[-3+4]
        data.at[index,'Probability_Octant_minus_3']=round(octant_values_frequency[-3+4]/N,3)
        max_min_update(octant_values_frequency[-3+4],-3)

        #for id 4
        data.at[index,'Octant_plus_4']=octant_values_frequency[4+4]
        data.at[index,'Probability_Octant_plus_4']=round(octant_values_frequency[4+4]/N,3)
        max_min_update(octant_values_frequency[4+4],4)

        #for id -4
        count_i=0
        data.at[index,'Octant_minus_4']=octant_values_frequency[-4+4]
        data.at[index,'Probability_Octant_minus_4']=round(octant_values_frequency[-4+4]/N,3)
        max_min_update(octant_values_frequency[-4+4],-4)
        
        #total octant
        data.at[index,'Total_Octant_sample']=N
except:
    print("Error in calling octant function")


try:
    def Acceleration_U(N):
        for i in range(N):
            if i==0:
                continue
            else:
                data.at[i,'accl_U']=(data.at[i,'U']-data.at[i-1,'U'])/data.at[1,'Time']
except:
    print("Error in calling Acceleration_U function")


try:
    def Acceleration_V(N):
        for i in range(N):
            if i==0:
                continue
            else:
                data.at[i,'accl_V']=data.at[i,'V']-data.at[i-1,'V']/data.at[1,'Time']
except:
    print("Error in calling Acceleration_V function")


try:
    def Acceleration_W(N):
        for i in range(N):
            if i==0:
                continue
            else:
                data.at[i,'accl_W']=data.at[i,'W']-data.at[i-1,'W']/data.at[1,'Time']
except:
    print("Error in calling Acceleration_W function")


try:
    def update_acceleration(N):
        Acceleration_U(N)
        Acceleration_V(N)
        Acceleration_W(N)
except:
    print("Error in calling update_acceleration function")


try:
    def find_std():
        data['U_std']=data['V_std']=data['W_std']=0.0
        data.at[0,'U_std']=data['U'].std()
        data.at[0,'V_std']=data['V'].std()
        data.at[0,'W_std']=data['W'].std()   
except:
    print("Error in calling find_std function")

try:
    def find_mean():
        data['U_mean']=data['V_mean']=data['W_mean']=0.0
        data.at[0,'U_mean']=data['U'].mean()
        data.at[0,'V_mean']=data['V'].mean()
        data.at[0,'W_mean']=data['W'].mean()
except:
    print("Error in calling find_mean function")


try:
    def replace_all_1(i):
        if i==0:
            return
        else:
            data.at[i,'U']=data.at[i-1,'U']
            data.at[i,'V']=data.at[i-1,'V']
            data.at[i,'W']=data.at[i-1,'W']
except:
    print("Error in calling replace_all function")

try:  
    def replace_U_1(i):
        if i==0:
            return
        else:
            data.at[i,'U']=data.at[i-1,'U']
except:
    print("Error in calling replace_U_1 function")

try:
    def replace_V_1(i):
        if i==0:
            return
        else:
            data.at[i,'V']=data.at[i-1,'V']
except:
    print("Error in calling replace_V_1 function")

try:
    def replace_W_1(i):
        if i==0:
            return
        else:
            data.at[i,'W']=data.at[i-1,'W']
except:
    print("Error in calling replace_W_1 function")


try:
    def replace_all_2(i):
        if i==0 or i==1:
            return
        else:
            data.at[i,'U']=2*data.at[i-1,'U']-data.at[i-2,'U']
            data.at[i,'V']=2*data.at[i-1,'V']-data.at[i-2,'V']
            data.at[i,'W']=2*data.at[i-1,'W']-data.at[i-2,'W']    
except:
    print("Error in calling replace_all_2 function")


try: 
    def replace_U_2(i):
        if i==0 or i==1:
            return
        else:
            data.at[i,'U']=2*data.at[i-1,'U']-data.at[i-2,'U']
except:
    print("Error in calling replace_U_2 function")


try:
    def replace_V_2(i):
        if i==0 or i==1:
            return
        else:
            data.at[i,'V']=2*data.at[i-1,'V']-data.at[i-2,'V']
except:
    print("Error in calling replace_V_2 function")

try:
    def replace_W_2(i):
        if i==0 or i==1:
            return
        else:
            data.at[i,'W']=2*data.at[i-1,'W']-data.at[i-2,'W']
except:
    print("Error in calling replace_W_2 function")

try:
    def replace_all_3(i):
        if i==0:
            return
        data.at[i,'U']=data.at[0,'U_mean']
        data.at[i,'V']=data.at[0,'V_mean']
        data.at[i,'W']=data.at[0,'W_mean']
except:
    print("Error in calling replace_all_3 function")

try:
    def replace_U_3(i):
        if i==0:
            return
        data.at[i,'U']=data.at[0,'U_mean']
except:
    print("Error in calling replace_U_3 function")

try:
    def replace_V_3(i):
        if i==0:
            return
        data.at[i,'V']=data.at[0,'V_mean']
except:
    print("Error in calling replace_V_3 function")

try:
    def replace_W_3(i):
        if i==0:
            return
        data.at[i,'W']=data.at[0,'W_mean']
except:
    print("Error in calling replace_W_3 function")


try:
    def replace_all_4(i,N):
        if i<=12 or i>N-12:
            return
        else:
            x1=i-12
            y1=i
            x2=i+1
            y2=i+13
            data.at[i,'U']=(data['U'].iloc[x1:y1].mean()+data['U'].iloc[x2:y2].mean())/2
            data.at[i,'V']=(data['V'].iloc[x1:y1].mean()+data['V'].iloc[x2:y2].mean())/2
            data.at[i,'W']=(data['W'].iloc[x1:y1].mean()+data['W'].iloc[x2:y2].mean())/2
except:
    print("Error in calling replace_all_4 function")

try:
    def replace_U_4(i,N):
        if i<12 or i>N-12:
            return
        else:
            x1=i-12
            y1=i
            x2=i+1
            y2=i+13
            data.at[i,'U']=(data['U'].iloc[x1:y1].mean()+data['U'].iloc[x2:y2].mean())/2
except:
    print("Error in calling replace_U_4 function")

try:
    def replace_V_4(i,N):
        if i<12 or i>N-12:
            return
        else:
            x1=i-12
            y1=i
            x2=i+1
            y2=i+13
            data.at[i,'V']=(data['V'].iloc[x1:y1].mean()+data['V'].iloc[x2:y2].mean())/2
except:
    print("Error in calling replace_V_4 function")

try:
    def replace_W_4(i,N):
        if i<12 or i>N-12:
            return
        else:
            x1=i-12
            y1=i
            x2=i+1
            y2=i+13
            data.at[i,'W']=(data['W'].iloc[x1:y1].mean()+data['W'].iloc[x2:y2].mean())/2
except:
    print("Error in calling replace_W_4 function")


def replace_all_5(i,N):
    if i==0 or i==N-1:
        return
    else:
        data.at[i,'U']=(data.at[i-1,'U']+data.at[i+1,'U'])/2
        data.at[i,'V']=(data.at[i-1,'V']+data.at[i+1,'V'])/2
        data.at[i,'W']=(data.at[i-1,'W']+data.at[i+1,'W'])/2
def replace_U_5(i,N):
    if i==0 or i==N-1:
        return
    else:
        data.at[i,'U']=(data.at[i-1,'U']+data.at[i+1,'U'])/2
def replace_V_5(i,N):
    if i==0 or i==N-1:
        return
    else:
        data.at[i,'V']=(data.at[i-1,'V']+data.at[i+1,'V'])/2
def replace_W_5(i,N):
    if i==0 or i==N-1:
        return
    else:
        data.at[i,'W']=(data.at[i-1,'W']+data.at[i+1,'W'])/2


def replace_all(i,x,N):
    if(x==1):replace_all_1(i)
    if(x==2):replace_all_2(i)
    if(x==3):replace_all_3(i)
    if(x==4):replace_all_4(i,N)
    if(x==5):replace_all_5(i,N)

def replace_U(i,x,N):
    if(x==1):replace_U_1(i)
    if(x==2):replace_U_2(i)
    if(x==3):replace_U_3(i)
    if(x==4):replace_U_4(i,N)
    if(x==5):replace_U_5(i,N)

def replace_V(i,x,N):
    if(x==1):replace_V_1(i)
    if(x==2):replace_V_2(i)
    if(x==3):replace_V_3(i)
    if(x==4):replace_V_4(i,N)
    if(x==5):replace_V_5(i,N)
        
def replace_W(i,x,N):
    if(x==1):replace_W_1(i)
    if(x==2):replace_W_2(i)
    if(x==3):replace_W_3(i)
    if(x==4):replace_W_4(i,N)
    if(x==5):replace_W_5(i,N)

def acceleration_all_at_a_time_negative(x,N):
    found_peak=1
    max_iteration=12
    while found_peak and max_iteration>0:
        update_acceleration(N)
        find_std()
        find_mean()
        max_iteration-=1
        found_peak=0
        for i in range(N):
            if i==0:
                continue
            if (data.at[i,'accl_U']<-1*Lambda*g and data.at[i,'U']<-1*data.at[0,'U_std']*k) or(data.at[i,'accl_V']<-1*Lambda*g and data.at[i,'V']<-1*data.at[0,'V_std']*k) or (data.at[i,'accl_W']<-1*Lambda*g and data.at[i,'W']<-1*data.at[0,'W_std']*k):
                found_peak=1
                replace_all(i,x,N)

def acceleration_one_at_a_time_negative(x,N):
    found_peak=1
    max_iteration=12
    while found_peak and max_iteration>0:
        update_acceleration(N)
        find_std()
        find_mean()
        max_iteration-=1
        found_peak=0
        for i in range(N):
            if i==0:
                continue
            if ((data.at[i,'accl_U']*1)<-1*Lambda*g) and ((data.at[i,'U']*1)<(-1*data.at[0,'U_std']*k)):
                found_peak=1
                replace_U(i,x,N)
            if ((data.at[i,'accl_V']*1)<-1*Lambda*g)and ((data.at[i,'V']*1)<(-1*data.at[0,'V_std']*k)):
                found_peak=1
                replace_V(i,x,N)
            if  ((data.at[i,'accl_W']*1)<-1*Lambda*g) and ((data.at[i,'W']*1)<-1*data.at[0,'W_std']*k):
                found_peak=1
                replace_W(i,x,N) 

def acceleration_all_at_a_time_positive(x,N):
    found_peak=1
    max_iteration=12
    while found_peak and max_iteration>0:
        update_acceleration(N)
        find_std()
        find_mean()
        max_iteration-=1
        found_peak=0
        for i in range(N):
            if i==0:
                continue
            if (data.at[i,'accl_U']>1*Lambda*g and data.at[i,'U']>1*data.at[0,'U_std']*k) or(data.at[i,'accl_V']>1*Lambda*g and data.at[i,'V']>1*data.at[0,'V_std']*k) or (data.at[i,'accl_W']>1*Lambda*g and data.at[i,'W']>1*data.at[0,'W_std']*k):
                found_peak=1
                replace_all(i,x,N) 
        
def acceleration_one_at_a_time_positive(x,N):
    found_peak=1
    max_iteration=12
    while found_peak and max_iteration>0:
        update_acceleration(N)
        find_std()
        find_mean()
        max_iteration-=1
        found_peak=0
        for i in range(N):
            if i==0:
                continue
            if ((data.at[i,'accl_U']*1)>1*Lambda*g) and ((data.at[i,'U']*1)>(1*data.at[0,'U_std']*k)):
                found_peak=1
                replace_U(i,x,N) 
            if ((data.at[i,'accl_V']*1)>1*Lambda*g)and ((data.at[i,'V']*1)>(1*data.at[0,'V_std']*k)):
                found_peak=1
                replace_V(i,x,N) 
            if  ((data.at[i,'accl_W']*1)>1*Lambda*g) and ((data.at[i,'W']*1)>1*data.at[0,'W_std']*k):
                found_peak=1
                replace_W(i,x,N)

def update_acceleration_one_at_time(x,N):
    acceleration_one_at_a_time_negative(x,N)
    acceleration_one_at_a_time_positive(x,N)
    
def update_acceleration_all_at_time(x,N):
    acceleration_all_at_a_time_negative(x,N)
    acceleration_all_at_a_time_positive(x,N)

def Corr_All(x,corr,N):
    for i in range(N):
        if i==0:
            continue
        if int(data.at[i,'Corr_U'])<int(corr) or int(data.at[i,'Corr_V'])<int(corr) or int(data.at[i,'Corr_W'])<int(corr):
            replace_all(i,x,N)

def Corr_One(x,corr,N):
    for i in range(N):
        if i==0:
            continue
        if int(data.at[i,'Corr_U'])<int(corr):
            replace_U(i,x,N)
        if int(data.at[i,'Corr_V'])<int(corr):
            replace_V(i,x,N)
        if int(data.at[i,'Corr_W'])<int(corr):
            replace_W(i,x,N)

def SNR_All(x,SNR,N):
    for i in range(N):
        if i==0:
            continue
        if int(data.at[i,'SNR_U'])<int(SNR) or int(data.at[i,'SNR_V'])<int(SNR) or int(data.at[i,'SNR_W'])<int(SNR):
            replace_all(i,x,N)

def SNR_One(x,SNR,N):
    for i in range(N):
        if i==0:
            continue
        if int(data.at[i,'SNR_U'])<int(SNR):
            replace_U(i,x,N)
        if int(data.at[i,'SNR_V'])<int(SNR):
            replace_V(i,x,N)
        if int(data.at[i,'SNR_W'])<int(SNR):
            replace_W(i,x,N)
            


def store():
    with open(r"Results_v2.csv",mode='a') as file_:
        file_.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(name,data.at[0,'U_mean'],data.at[0,'V_mean'],data.at[0,'W_mean'],data.at[0,'Var_u\''],data.at[0,'Var_v\''],data.at[0,'Var_w\''],data.at[0,'std_u\''],data.at[0,'std_v\''],data.at[0,'std_w\''],data.at[0,'Skewness_u\''],data.at[0,'Skewness_v\''],data.at[0,'Skewness_w\''],data.at[0,'Kurtosis_u\''],data.at[0,'Kurtosis_v\''],data.at[0,'Kurtosis_w\''],data.at[0,'Reynolds_stress_u\'v\''],data.at[0,'Reynolds_stress_u\'w\''],data.at[0,'Reynolds_stress_v\'w\''],data.at[0,'anisotropy'],data.at[0,'M30'],data.at[0,'M03'],data.at[0,'M12'],data.at[0,'M21'],data.at[0,'fku_2d'],data.at[0,'Fku_2d'],data.at[0,'fkw_2d'],data.at[0,'Fkw_2d'],data.at[index,'fku_3d'],data.at[index,'Fku_3d'],data.at[index,'fkw_3d'],data.at[index,'Fkw_3d'],data.at[index,'TKE_3D'],data.at[0,'Q1_K_Value'],data.at[0,'Q2_K_Value'],data.at[0,'Q3_K_Value'],data.at[0,'Q4_K_Value'],0,0,data.at[0,'Octant_plus_1'],data.at[0,'Octant_minus_1'],data.at[0,'Octant_plus_2'],data.at[0,'Octant_minus_2'],data.at[0,'Octant_plus_3'],data.at[0,'Octant_minus_3'],data.at[0,'Octant_plus_4'],data.at[0,'Octant_minus_4'],data.at[0,'Total_Octant_sample'],data.at[0,'Probability_Octant_plus_1'],data.at[0,'Probability_Octant_minus_1'],data.at[0,'Probability_Octant_plus_2'],data.at[0,'Probability_Octant_minus_2'],data.at[0,'Probability_Octant_plus_3'],data.at[0,'Probability_Octant_minus_3'],data.at[0,'Probability_Octant_plus_4'],data.at[0,'Probability_Octant_minus_4'],data.at[0,'Min_Octant_Count'],data.at[0,'Min_Octant_Count_id'],data.at[0,'Max_Octant_Count'],data.at[0,'Max_Octant_Count_id'],"\n"))

def allfunction(N):
    useful_values()
    fk()
    Q_K_Value()
    octant(N)



def add_front_name(name,x):
    if(x==1):name = name + "_previous_point"
    if(x==2):name = name + "_2*last-2nd_last"
    if(x==3):name = name + "_overall_mean"
    if(x==4):name = name + "_12_point_strategy"
    if(x==5):name = name + "_mean_of_previous_2point"
    
    print(name)
    return name


end_time = datetime.now()

print("-------------------------------------------------------------------")
print("\nStart Time :", start_time.strftime("%c"))
print("\nEnd Time :", end_time.strftime("%c")) 
print('\nDuration: {}'.format(end_time - start_time))
duration=end_time - start_time
name="Complete Duration"
duration_timestamp_to_file(name, duration)

print("-------------------------------------------------------------------")



###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


proj_psat_gui()






#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))