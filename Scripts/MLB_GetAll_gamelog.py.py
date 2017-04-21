import re
import os
import commands
from BeautifulSoup  import BeautifulSoup
import time
from datetime import datetime

os.system('rm AllPlayers.txt')
file1 = open('AllTeams.html','r')
soup = BeautifulSoup(file1)

file2 = open('AllPlayers.txt','w+')

file41 = open('AllPlayersPitching.txt','w+')
# file4 = open('AllPlayersNew_2017.txt','ab+')

def GameLogs(link,playerName,type_B_P,position):
	if len(link) < 4:
		return

	curlLink = 'curl "http://www.baseball-reference.com/players/gl.fcgi?id=' + link + '&t='+type_B_P[0]+'&year=2016"'
	print curlLink
	os.system('%s > Team_Bat.txt'% (curlLink))

	file31 = open('Team_Bat.txt','r')
	flag = 0
	DivTag=""
	for each in file31:

		if flag ==1:
			DivTag = DivTag + each

		if re.match(".*(all_batting_gamelogs|div_pitching_gamelogs).*",each):
			DivTag = DivTag + each
			flag = 1

	file31.close()
	data_line_Insert = ""

	newSoup = BeautifulSoup(DivTag)
	Souphref=""
	if newSoup.find('div', id='div_batting_gamelogs'):
		Souphref = newSoup.find('div', id='div_batting_gamelogs')
	else:
		Souphref = newSoup.find('div', id='div_pitching_gamelogs')

	playerStats =   data_line_Insert +'\''+ playerName + '\''+ ','
	# print "HERE"
	if len (str(Souphref)) < 300:
		return
	##### collect tds
	newTable = ""
	for trs in Souphref.findAll('tr'):
		tempStats = ""
		# print trs

		for ths in trs.findAll('th'):
			if re.match('.*Rk.*',ths.text):
				# print ths
				flagT = 1
				# input()
		if flagT == 1:
			newTable = newTable + str(trs)
		for tds in trs.findAll('td'):	
			# print tds
			if flagT == 1:
				newTable = newTable + str(tds)

	sS = BeautifulSoup(newTable)
	headings = [th.text for th in sS.find("tr").findAll("th")]
	newHeadings =[]
	newHeadings.append('playerId')
	newHeadings.append('position')
	newHeadings.append('playerName')
	for each in headings:
		if len(each) > 15:
			newHeadings.append(each.split(';')[-1])
		else:
			newHeadings.append(each)

	sSql = "insert into `mlb`.`"+type_B_P+"` ("

	L = len(newHeadings)
	l = 0
	for each in newHeadings:
		if not re.match('.*\+.*', each):	
			regex = re.compile(r".*%s.*"%each)
			if regex.match((sSql)):				
				l = l + 1				
				sSql =  sSql + '`' + each + 'RP'+ str(l) + '`,'
			else:
				sSql =  sSql + '`' + each + '`,'
		else:
			sSql =  sSql + '`' + 'plusMinus' + '`,'
	sSql= sSql[:-1] + ') values ('

	datasets = []
	allTds = []
	allTds.append(link)
	allTds.append(position)
	allTds.append(playerName)
	allTds.append(1)
	### add 1 in begging to fix the odering
	for row in sS.findAll("tr")[1:]:

		for td in row.findAll("td"):
			
			if re.match('.*Player Suspended.*',str(td) ):
				# t = ",'','','','','','','','','','','','','','','','','','','','','','','' "
				for i in range(0,37):
					allTds.append(0)
				# print td
				# input()
				break
		

			if re.match('.*Inactive.*',str(td) ):
				# t = ",'','','','','','','','','','','','','','','','','','','','','','','' "
				for i in range(0,L-4):
					allTds.append(0)
				# print td
				# input()
				break
			if re.match('.*Did Not Dress.*',str(td) ):
				# t = ",'','','','','','','','','','','','','','','','','','','','','','','' "
				for i in range(0,L-4):
					allTds.append(0)
				# print td
				# input()
				break		

			if re.match('.*Not With.*',str(td) ):
				# t = ",'','','','','','','','','','','','','','','','','','','','','','','' "
				for i in range(0,L-4):
					allTds.append(0)
				# print td
				# input()
				break		

			if re.match('.*Did Not Play.*',str(td) ): 
				# print td
				for i in range(0,L-4):
					allTds.append(0)
				# input()
				break

			if re.match('.*Player went.*',str(td) ): 
				# print td
				for i in range(0,L-4):
					allTds.append(0)
				# input()
				break
			allTds.append(td.text.replace('(','').replace(')','') )
			# input()
		
		dataset = zip(newHeadings, allTds)
		allTds = []
		allTds.append(link)
		allTds.append(position)
		allTds.append(playerName)
		allTds.append(1)

		datasets.append(dataset)

	whenToBrace = 0

	######### collecting all gamelogs
	for dataset in datasets:
		# print dataset
		# print len(dataset)
		# input()
		if len(dataset) > 10:
			for field in dataset:
				sSql = sSql + '\'' + str(field[1]) + '\','
			    # print "{0:<16}: {1}".format(field[0], field[1])

				if whenToBrace == len(dataset)-1 :
					sSql = sSql[:-1]
					sSql = sSql + '),\n ('
					# print sSql
					whenToBrace = 0
				else:
					whenToBrace =whenToBrace + 1

	print sSql[:-4]
	file2.write(sSql[:-4] + ';\n')

def BattingStats(link):
	if len(link) < 4:
		return
	curlLink = 'curl http://www.baseball-reference.com' + link + '2016.shtml'
	os.system('%s > TeamAll.txt'% (curlLink))

	file12 = open('TeamAll.txt','r')
	flag = 0
	DivTag=""

	# print file2
	for each in file12:
		# print each
		if flag ==1:
			DivTag = DivTag + each

		if re.match(".*div_team_batting.*",each):
			# print each
			DivTag = DivTag + each
			flag = 1


	newSoup = BeautifulSoup(DivTag)
	# print newSoup
	Souphref = newSoup.find("div", id="div_team_batting")

	# print Souphref
	# input()
	i = 0
	if len (str(Souphref)) < 300:
		return
		
	for hrefs in Souphref.findAll('a'):
		# if i > 20:
			# break
		
		if re.match(".*<a href=\"/players",str(hrefs)):
			tt =    hrefs.text
			print hrefs.text
			temp = (((hrefs.parent).parent).findNext('td'))
			print temp.text
			# input()
			GameLogs( hrefs['href'].split('/')[-1].split('.')[0],tt,"batter",temp.text )

			i = i + 1


def PitchingStats(link):
	if len(link) < 4:
		return
	curlLink = 'curl http://www.baseball-reference.com' + link + '2016.shtml'
	print curlLink
	os.system('%s > TeamAll.txt'% (curlLink))

	file12 = open('TeamAll.txt','r')
	flag = 0
	DivTag=""

	# print file2
	for each in file12:
		# print each
		if flag ==1:
			DivTag = DivTag + each

		if re.match(".*div_team_pitching.*",each):
			# print each
			DivTag = DivTag + each
			flag = 1


	newSoup = BeautifulSoup(DivTag)
	Souphref = newSoup.find("div", id="div_team_pitching")

	i = 0
	if len (str(Souphref)) < 300:
		return
		
	for hrefs in Souphref.findAll('a'):
		if i > 25:
			break
		tt =    hrefs.text
		temp = (((hrefs.parent).parent).findNext('td'))
		GameLogs( hrefs['href'].split('/')[-1].split('.')[0],tt,"pitcher",temp.text )


		i = i + 1


DIV = soup.find("div", id="div_active")
AllTeams = []

for hrefs in DIV.findAll('a'):
	if re.match('.*/teams/.*',str(hrefs)) and not re.match('.*class.*',str(hrefs)):
		AllTeams.append(hrefs['href'])

for i in range(0,len(AllTeams)):
	BattingStats(AllTeams[i])
	PitchingStats(AllTeams[i])

BattingStats('/teams/LAA/')
PitchingStats('/teams/LAA/')

BattingStats('/teams/MIA/')
PitchingStats('/teams/MIA/')