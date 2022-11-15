# Libraries...
import os 
os.system('cls')
import re
import numpy as np
import math

from datetime import datetime
start_time = datetime.now()

#Help
def scorecard():
	try:
		try:
			file1 = open("Scorecard.txt","w")
		except:
			print("Error in opening Scorecard Text file...")

		# Static file list...
		list_of_files = ['teams.txt','pak_inns1.txt','india_inns2.txt']

		# Fetched team details from "teams.txt"...
		team_names = []
		team = {}

		try:
			with open(list_of_files[0]) as f:
				content = f.readlines()
				for line in content:
					if len(re.split(": ",line)) != 1:
						if re.split(r"\s+",line,1)[0] not in team:
							team[re.split(r"\s+",line,1)[0]] = 0
						
						team_member = re.split(", ",(re.split(": ",line)[1]))
						team_member[len(team_member)-1] = team_member[len(team_member)-1][:-1]
						team[re.split(r"\s+",line,1)[0]] = team_member
						team_names.append(re.split(r"\s+",line,1)[0])
		except:
			print("Error in opening \"teams\" text file...")
		
		# "for" loop on Pakistan-India Innings-Text-file
		for i in list_of_files[1:]:
			powerplay_runs = 0

			try:
				with open(i) as f:
					content = f.readlines() 

					# Variables to store Batsman and Bowler's data
					list_of_bowler = {}
					list_of_batter = {}
					extras = [0,0,0] # B, LB, P
					# out_sequence variable is used to store sequence in which batsman gets out during the match.
					out_sequence = {}

					x = 1
					for line in content:
						# Check for No Ball, M Counts Later
						if re.split(r"\s+",re.split(r" to",line,1)[0],1)[1] not in list_of_bowler:
							list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]] = [0,0,0,0,0,0,0,0] # O M R W NB WD Ball_count_in_over

						if re.split(r"to |,",line)[0] != '\n':
							if re.split(r"to |,",line)[1] not in list_of_batter:
								list_of_batter[re.split(r"to |,",line)[1]] = [0,0,0,0,0,0] #wicket_taken_by R B 4s 6s, out on which ball

						# Dot Balls =================================
						if re.split(r", |,",line)[0] != '\n':
							# To count no run on a particular ball ====================================
							if re.split(r", |,",line)[1] == 'no run':
								list_of_batter[re.split(r"to |,",line)[1]][1] += 0
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1 

								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][2] += 0    

							# To count 1 run on a particular ball ====================================                
							elif re.split(r", |,",line)[1] == '1 run':
								list_of_batter[re.split(r"to |,",line)[1]][1] += 1
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1

								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][2] += 1

							# To count 2 runs on a particular ball ====================================
							elif re.split(r", |,",line)[1] == '2 runs':
								list_of_batter[re.split(r"to |,",line)[1]][1] += 2
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1

								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][2] += 2

							# To count 3 runs on a particular ball ====================================
							elif re.split(r", |,",line)[1] == '3 runs':
								list_of_batter[re.split(r"to |,",line)[1]][1] += 3
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1

								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][2] += 3

							# To count 4 runs on a particular ball ====================================
							elif re.split(r", |,",line)[1] == 'FOUR':
								list_of_batter[re.split(r"to |,",line)[1]][1] += 4
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1
								list_of_batter[re.split(r"to |,",line)[1]][3] += 1

								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][2] += 4

							# To count 6 runs on a particular ball ====================================
							elif re.split(r", |,",line)[1] == 'SIX':
								list_of_batter[re.split(r"to |,",line)[1]][1] += 6
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1
								list_of_batter[re.split(r"to |,",line)[1]][4] += 1

								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][2] += 6

							# To count wide runs and wide balls for a particular bowler ====================================
							elif re.split(r", |,",line)[1] == 'wide':
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][5] += 1
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][6] -= 1
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][7] -= 1
							elif re.split(r", |,",line)[1] == '2 wides':
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][5] += 2
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][6] -= 1
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][7] -= 1
							elif re.split(r", |,",line)[1] == '3 wides':
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][5] += 3
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][6] -= 1
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][7] -= 1

							# To count byes on a particular ball ====================================
							elif re.split(r", |,",line)[1] == 'byes':
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1
								# print(line[0:4],re.split(r", |,",line))
								if re.split(r", |,",line)[2] == '1 run':
									extras[0] += 1
								if re.split(r", |,",line)[2] == '2 runs':
									extras[0] += 2
								if re.split(r", |,",line)[2] == '3 runs':
									extras[0] += 3
								if re.split(r", |,",line)[2] == 'FOUR':
									extras[0] += 4

							# To count leg byes on a particular ball ====================================
							elif re.split(r", |,",line)[1] == 'leg byes':
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1
								# print(line[0:4],re.split(r", |,",line)[1])
								if re.split(r", |,",line)[2] == '1 run':
									extras[1] += 1
								if re.split(r", |,",line)[2] == '2 runs':
									extras[1] += 2
								if re.split(r", |,",line)[2] == '3 runs':
									extras[1] += 3
								if re.split(r", |,",line)[2] == 'FOUR':
									extras[1] += 4
								
							# To check on which condition batsman is getting out i.e. (caught by, lbw, bowled) on a particular ball ====================================
							elif re.split(r"\s+", re.split(r", |,",line)[1])[0] == 'out':
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][3] += 1
								bowler = re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]
								list_of_batter[re.split(r"to |,",line)[1]][5] = re.split(r"\s+",line,1)[0]
								list_of_batter[re.split(r"to |,",line)[1]][2] += 1 
								
								if "Caught by" in line:
									caught = line.split("Caught by ",1)[1].split("!!",1)[0]
									# caught = re.split(r"to |,",line)[1]
									list_of_batter[re.split(r"to |,",line)[1]][0] = f"c {caught} b {bowler}"	
								elif "Lbw" in line:
									list_of_batter[re.split(r"to |,",line)[1]][0] = f"lbw b {bowler}"
								elif "Bowled" in line:
									list_of_batter[re.split(r"to |,",line)[1]][0] = f"b {bowler}"

								# Updating out_sequence on a particular ball ====================================
								if re.split(r"to |,",line)[1] not in out_sequence:
									out_sequence[re.split(r"to |,",line)[1]] = [0,0]

								out_sequence[re.split(r"to |,",line)[1]][0] = sum([x[2] for x in list(list_of_bowler.values())]) + sum([x[4] for x in list(list_of_bowler.values())]) + sum([x[5] for x in list(list_of_bowler.values())]) + sum(extras)
								out_sequence[re.split(r"to |,",line)[1]][1] = x
								x += 1

							
							# Calculating powerplay runs ====================================
							if sum([x[0] for x in list(list_of_bowler.values())]) == 5:
								powerplay_runs = sum([x[2] for x in list(list_of_bowler.values())]) + sum([x[4] for x in list(list_of_bowler.values())]) + sum([x[5] for x in list(list_of_bowler.values())]) + sum(extras)
							
							# Updating Number of Overs bowled by particular bowler ====================================
							list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][6] += 1
							if list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][6] == 6:
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][0] += 1
								list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][6] = 0
							
							list_of_bowler[re.split(r"\s+",re.split(r" to",line,1)[0],1)[1]][7] += 1


					# print(list_of_bowler)
					for i in list_of_bowler.keys():
						if list_of_bowler[i][6] != 0:
							s = f'{list_of_bowler[i][0]}.{list_of_bowler[i][6]}'
							list_of_bowler[i][0] = float(s)

					del list_of_bowler['']

					# Calculating total score of the team ====================================
					total_score = sum([x[2] for x in list(list_of_bowler.values())]) + sum([x[4] for x in list(list_of_bowler.values())]) + sum([x[5] for x in list(list_of_bowler.values())]) + sum(extras)
					# print(list_of_bowler)
					name = team_names[0] + ' Innings'
					file1.write(f"{name :<96}{total_score}-{sum([x[3] for x in list(list_of_bowler.values())])} ({line[0:4]} Ov)\n")

					line1 = f"{'Batter' : <55}{'R' : ^20}{'B' : >2}{'4s' : >10}{'6s' : >10}{'SR' : >15}\n"
					file1.write(line1)


					# Mapping team member name to their full name present in the teams.txt file ====================================
					mapped_list_of_batter = {}
					for i in list_of_batter.keys():
						for j in team[team_names[0]]:
							if i in j:
								# print(i,j)  
								mapped_list_of_batter[j] = list_of_batter[i]
							else:
								continue

					# print(mapped_list_of_batter)
					# Updating Batting performance of the team ====================================
					for i in mapped_list_of_batter.keys():
						if mapped_list_of_batter[i][0] == 0:
							mapped_list_of_batter[i][0] = "not out"
						line1 = (f"{i : <20}{mapped_list_of_batter[i][0] : <35}{mapped_list_of_batter[i][1] : ^20}{mapped_list_of_batter[i][2] : >2}{mapped_list_of_batter[i][3] : >10}{mapped_list_of_batter[i][4] : >10}{np.round((mapped_list_of_batter[i][1]/mapped_list_of_batter[i][2])*100,decimals=2) : >15}\n")
						file1.write(line1)
					len_of_string = len(line1)

					# =============================================================================
					ex = f"(b {extras[0]}, lb {extras[1]}, w {sum([x[5] for x in list(list_of_bowler.values())])}, nb {sum([x[4] for x in list(list_of_bowler.values())])}, p {extras[2]})"
					file1.write(f"{'Extras' : <62}{sum([x[4] for x in list(list_of_bowler.values())]) + sum([x[5] for x in list(list_of_bowler.values())]) + sum(extras) : ^5}{ex : >2}\n")

					# =============================================================================
					wk_ov = f"({sum([x[3] for x in list(list_of_bowler.values())])} wkts, {line[0:4]} Ov)"
					file1.write(f"{'Total' : <62}{total_score : ^5}{wk_ov : >2}\n")

					# Updating Did not Bat row in the scorecard file ==============================
					if sum([x[3] for x in list(list_of_bowler.values())]) != 10:
						line = f"{'Did not Bat' : <20}"
						for i in team[team_names[0]]:
							if i not in mapped_list_of_batter.keys():
								if team[team_names[0]].index(i) == len(team[team_names[0]])-1:
									line += i 
								else:
									line += i + ", "
						line += "\n\n"
						file1.write(line)
					else: 
						file1.write("\n")


					if len(team_names) != 1:
						del team_names[0]


					# =================================Fall of Wickets====================================
					file1.write("Fall of Wickets\n")

					line1 = ''
					for i in out_sequence.keys():
						line2 = f"{out_sequence[i][0]}-{out_sequence[i][1]} ({i}, {list_of_batter[i][5]}), "
						line1 += line2
					line1 = line1[:len(line1)-2]
					# print(line1)

					lens = []
					len_of_line1 = len(line1)
					n = math.ceil(len_of_line1/len_of_string)
					for i in range(n):
						if len_of_line1 > len_of_string:
							lens.append(len_of_string)
							len_of_line1 -= len_of_string
						else:
							lens.append(len_of_line1)


					line3 = []
					x = 0
					for i in range(len(lens)):
						if i+1 == len(lens):
							string = line1[x:]
						else:
							string = line1[x:lens[i]+x+1]
							x += lens[i]+1
						line3.append(string)
				

					for z in line3:
						line = z+"\n"
						file1.write(line)

					# Updating Bowling performance of the respective team ====================================
					line1 = f"\n{'Bowler' : <35}{'O' : ^20}{'M' : >2}{'R' : >10}{'W' : >10}{'NB' : >10}{'WD' : >10}{'ECO' : >15}\n"
					file1.write(line1)
					
					for i in list_of_bowler.keys():
						line1 = f"{i : <35}{list_of_bowler[i][0] : ^20}{list_of_bowler[i][1] : >2}{list_of_bowler[i][2]+list_of_bowler[i][5] : >10}{list_of_bowler[i][3] : >10}{list_of_bowler[i][4] : >10}{list_of_bowler[i][5] : >10}{np.round(((list_of_bowler[i][2]+list_of_bowler[i][5])/list_of_bowler[i][7])*6,1) : >15}\n"
						file1.write(line1)
					
					# ========================================================================================
					file1.write(f"\n{'Powerplays' :<46}{'Overs' : ^20}{'Runs' : >46}\n")
					file1.write(f"{'Mandatory' :<46}{'0.1-6' : ^20}{powerplay_runs : >46}\n\n")
		
			except:
				print("Error in opening \"Pak-Ind Innings\" text file...")
	except:
		print("Error in calling scorecard function")
		


###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


scorecard()


#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
