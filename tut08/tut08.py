import os 
os.system('cls')
import re
import numpy as np
import math

from datetime import datetime
start_time = datetime.now()

#Help
def scorecard():
	file1 = open("Scorecard.txt","w")

	list_of_files = ['teams.txt','pak_inns1.txt','india_inns2.txt']

	team_names = []
	team = {}
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
	print(team_names,team)


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
