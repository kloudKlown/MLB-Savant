import re
import os
import commands
from BeautifulSoup  import BeautifulSoup
import Levenshtein
from time import sleep
from datetime import datetime
 
# file1 = open('All_2016_Players.html','r')
 
# BB_reference="http://www.basketball-reference.com"
# playerName_URL = ""
# playerName = ""
 
PlayerIDS = []
PlayerNamesCSV = []
PlayerNamesWeb = []
### HITTERS
# url = ['http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type=\'R\'&season=2016&season_type=ANY&league_code=\'MLB\'&sectionType=sp&statType=hitting&page=1&timeframe=d7&split=&last_x_days=7',
    # 'http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type=\'R\'&season=2016&season_type=ANY&league_code=\'MLB\'&sectionType=sp&statType=hitting&page=2&timeframe=d7&split=&last_x_days=7',
    # 'http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type=\'R\'&season=2016&season_type=ANY&league_code=\'MLB\'&sectionType=sp&statType=hitting&page=3&timeframe=d7&split=&last_x_days=7',
    # 'http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type=\'R\'&season=2016&season_type=ANY&league_code=\'MLB\'&sectionType=sp&statType=hitting&page=4&timeframe=d7&split=&last_x_days=7']
sql_Create_PlayerList=" insert into mlb.player_id (player_id,player_name,player_link) values "
# rendermulti-1.pngtest
sql_Create_7DayList = ""
 
tmp = "INSERT INTO `mlb`.`player_stats` (`player_id`,`player_name`,`team_name`,`position`,`games_played`, `at_bats`,`runs`,`hits`,`second_base`,`third_base`,`home_runs`,`rbi`,`bb`,`ko`,`stolen`,`caught`,`avg`,`obp`, `slg`,`ops`,`ibb`,`hbp`,`sac`,`sf`,`tb`,`xbp`,`gdp`,`go`,`ao`,`goao`,`np`,`pa`,`day`) VALUES "
 
sql_Create_7DayList = sql_Create_7DayList + tmp + '\n'
 
file3 = open('7dayInsert.sql','ab+')
file4 = open('players1TIME.sql','ab+')
 
begD = datetime(2016,01,01)
todD = datetime.now()
 
diffD = todD - begD
 
diffD = diffD.days
 
for each in range(1,7):
 
    # print each
 
    # os.system('./phantomjs.exe loadurlwithoutcss.js %s'%(each))
    link = 'rendermulti-'+str(each)+'.pngtest.html'
    # print link
    file1= open(link,'r')   
    # print file1
    soup = BeautifulSoup(file1)
    # print soup
    # input()
    td = soup.find('div',id='datagrid')
 
    # hrefs = soup.findAll('a',)
    for href in td.findAll('a', href= True):
        print str(href['href']) + ',' + href.text
        pid =  str(href['href']).split('=')[-1]
        insert = '(\'' + pid \
            + '\',\'' + href.text + '\',\'' + 'https://baseballsavant.mlb.com/player?player_id='+ pid + '&player_type=batter' + '\'),'
        # print insert
        # sql_Create_PlayerList.append(insert)
        sql_Create_PlayerList = sql_Create_PlayerList + insert + '\n'
 
    _7day = ""
    for tdss in td.findAll('td'):
 
        if re.match('.*href.*',str(tdss)):
            # print tdss
            pid =  str(tdss.find('a',href=True)).split('=')[-1]
            # print pid
            pid = pid.split('">')[0]
            # print pid
            if len(_7day) > 5:
                 
                print _7day
                temp = _7day.split('&nbsp;')
                temp2 = temp[1].split(',')
 
                temp2 =  '\'' + temp2[0] + temp2[1] + '\',\'' + temp2[2] + '\','
 
                _7day =  '(' + temp[0] + temp2 + '\'' + temp[2][8:10] + '\',' + temp[2][11:] +',' +str(diffD) +  '),'
                print _7day
                # input()
                # sql_Create_7DayList.append(_7day)\
                sql_Create_7DayList = sql_Create_7DayList + _7day + '\n'
                _7day = ""
 
            _7day = pid
 
 
        # print tdss.text
        _7day = _7day +',' + tdss.text
 
        # input()
 
 
file3.write((sql_Create_7DayList) )
