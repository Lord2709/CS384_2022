import os
os.system("cls")
import pandas as pd
import numpy as np
import datetime

# from datetime import datetime
start_time = datetime.datetime.now()

current_dir = os.getcwd()
path = current_dir.replace('\\','/') + "/output/"

if os.path.isdir("output"):
    list_of_files = os.listdir('output')
    for files in list_of_files:
        os.remove(path + f"{files}")
    os.rmdir("output")
os.mkdir(path)


def attendance_report():
    reg_stud = pd.read_csv("input_registered_students.csv")
    attendance = pd.read_csv("input_attendance.csv")

    attendance['Date'] = pd.to_datetime(attendance['Timestamp'], dayfirst=True).dt.date
    attendance['Time'] = pd.to_datetime(attendance['Timestamp']).dt.time
    attendance['Hour'] = pd.to_datetime(attendance['Timestamp']).dt.hour
    attendance['Min'] = pd.to_datetime(attendance['Timestamp']).dt.minute
    attendance['Sec'] = pd.to_datetime(attendance['Timestamp']).dt.second

    attendance['Date'] = attendance['Date'].astype(str)
    attendance['Time'] = attendance['Time'].astype(str)
    
    attendance = attendance.drop("Timestamp",axis = 1)

    roll_name = attendance['Attendance']
    rollno = []
    name = []
    for i in range(len(roll_name)):
        s = str(roll_name[i])
        rollno.append(s[:8])
        name.append(s[9:])
    attendance['Roll No'] = rollno
    attendance['Name'] = name
   
    attendance = attendance.drop("Attendance",axis = 1)

    roll = reg_stud['Roll No']
    name = reg_stud['Name']

    unique_date = set(attendance['Date'])
    unique_date_list = list(unique_date)


from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


attendance_report()




#This shall be the last lines of the code.
end_time = datetime.datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
