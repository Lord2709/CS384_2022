# Libraries...
import os
os.system("cls")
import pandas as pd
import numpy as np
import datetime

# from datetime import datetime
start_time = datetime.datetime.now()


global calendar_ls
calendar_ls = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def findDay(date):
    day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar_ls[day])


current_dir = os.getcwd()
path = current_dir.replace('\\','/') + "/output/"

if os.path.isdir("output"):
    list_of_files = os.listdir('output')
    for files in list_of_files:
        os.remove(path + f"{files}")
    os.rmdir("output")
os.mkdir(path)


def attendance_report():
    try:
        # reg_stud, attendance variables are used to store entire dataset.
        try:
            reg_stud = pd.read_csv("input_registered_students.csv")
            attendance = pd.read_csv("input_attendance.csv")
        except:
            print("Error : Failed to read Input Files...")

        # Converted Date column in attendance to "Datetime" datatype
        attendance['Date'] = pd.to_datetime(attendance['Timestamp'], dayfirst=True).dt.date

        # Made 4 extra columns storing Time, Hour, Minute and Seconds from timestamp separately in attendance variable
        attendance['Time'] = pd.to_datetime(attendance['Timestamp']).dt.time
        attendance['Hour'] = pd.to_datetime(attendance['Timestamp']).dt.hour
        attendance['Min'] = pd.to_datetime(attendance['Timestamp']).dt.minute
        attendance['Sec'] = pd.to_datetime(attendance['Timestamp']).dt.second

        # Converted Date and Time column to string datatype
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

        # Stored roll number and name from registered_students dataset into roll, name variable respectively
        roll = reg_stud['Roll No']
        name = reg_stud['Name']

        unique_date = set(attendance['Date'])
        unique_date_list = list(unique_date)

        total_lecture = 0
        class_date = []

        # Stored the class dates in class_date list and counted total number of lectures taken on Monday's and Thursday's
        try: 
            for i in unique_date_list:
                day = findDay(i)
                if day == 'Monday' or day == 'Thursday':
                    total_lecture += 1
                    class_date.append(i)

            class_date.sort()
        except:
            print("Error : Incorrect date format")


        row1 = ["Date","Roll",'Name','Total Attendance Count','Real','Duplicate','Invalid','Absent']
        header = ["Roll","Name"] + class_date + ["Actual Lecture Taken","Total Real","% Attendance"]

        # Overall_attendance dictionary is created to store data of all the students registered for the course
        Overall_attendance = {}
        for y in header:
            if y not in Overall_attendance:
                Overall_attendance[y] = []
        
        
        # This "for" loop is used to create individual attendance report
        for i in range(len(roll)):
            individual_list = []

            os.chdir(path)
            filename1 = f"{roll[i]}.xlsx"

            individual_list.append(["",roll[i],name[i],"","","","",""])
            
            # df_stud holds the dataframe with value of the particular roll number only.
            df_stud = attendance[attendance['Roll No']==roll[i]]
            date_list = df_stud['Date'].to_list()
            hour_list = df_stud['Hour'].to_list()
            minutes_list = df_stud['Min'].to_list()
            seconds_list = df_stud['Sec'].to_list()

            # date dictionary is used to store count of 'Total Attendance Count','Real','Duplicate','Invalid','Absent' respectively for each student registered
            date = {}
            for j in range(len(class_date)):
                # day list is used to store entire row of the individual report dataset
                day = [f"{class_date[j]}","",""]
                date[class_date[j]] = [0,0,0,0,0]
                for k in range(len(date_list)):
                    if (class_date[j] == date_list[k]):
                        if (hour_list[k] == 14):
                            date[class_date[j]][0] += 1
                            if date[class_date[j]][1] < 1:
                                date[class_date[j]][1] += 1
                            else:
                                date[class_date[j]][2] += 1
                        elif (hour_list[k] == 15) and (minutes_list[k]==0) and (seconds_list[k]==0):
                            date[class_date[j]][0] += 1
                            if date[class_date[j]][1] < 1:
                                date[class_date[j]][1] += 1
                            else:
                                date[class_date[j]][2] += 1
                        else:
                            date[class_date[j]][0] += 1
                            date[class_date[j]][3] += 1
                if date[class_date[j]][1] == 0:
                    date[class_date[j]][4] += 1
                
                day = day + date[class_date[j]]
                individual_list.append(day)
            

            individual_file_dict = {}
            for m in row1:
                if m not in individual_file_dict:
                    individual_file_dict[m] = []
                for z in individual_list:
                    if len(z) == 0:
                        continue
                    individual_file_dict[m].append(z[0])
                    del z[0]

            # ".to_excel" function of pandas is used to convert the dataframe into xlsx file
            try:
                df_individual_file = pd.DataFrame.from_dict(individual_file_dict)
                df_individual_file.to_excel(filename1, index = False)
            except:
                print("Error in generating Individual Attendance Report file")

            Overall_attendance['Roll'].append(roll[i])
            Overall_attendance['Name'].append(name[i])
            real = 0

            # if the real attendance on that particular class date is "1" then appending "P" to the Overall_attendance dictionary for that particular registered student only
            for l in range(len(class_date)):
                if date[class_date[l]][1] == 1:
                    Overall_attendance[class_date[l]].append('P')
                else:
                    Overall_attendance[class_date[l]].append('A')
                real = real + int(date[class_date[l]][1])
            Overall_attendance['Actual Lecture Taken'].append(len(class_date))

            Overall_attendance['Total Real'].append(real)
            Overall_attendance['% Attendance'].append(round((real/len(class_date))*100,2))
        
        # ".to_excel" function of pandas is used to convert the dataframe into xlsx file
        # Final report has been created.
        try:
            consolidated_file = pd.DataFrame.from_dict(Overall_attendance)
            consolidated_file.to_excel('attendance_report_consolidated.xlsx', index = False)
        except:
            print("Error : It seems that attendance_report_consolidated file has not been generated.")
    except:
        print("Error in calling function")


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
