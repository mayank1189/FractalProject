# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:22:59 2019

@author: Mayank
"""

import repositoryP as repo
import numpy as np
import matplotlib.pyplot as plot
import pandas as pd

matchesDF = repo.match_df
teamsDF = repo.team_df
seasonsDF = repo.season_df

data= pd.DataFrame(columns=('team_id','short_name','matches','wins','season_id','win_percent'))

def numMatchesPerTeamPerSeason(team_id, season_id):
    return matchesDF[((matchesDF['Team_Name_Id']==team_id) | (matchesDF['Opponent_Team_Id']==team_id)) & (matchesDF['Season_Id']==season_id)]
 
def numMatchesWonByTeamInSeason(team_id,season_id):
    return matchesDF[((matchesDF['Team_Name_Id']==team_id) | (matchesDF['Opponent_Team_Id']==team_id)) & (matchesDF['Season_Id']==season_id) & (matchesDF['Match_Winner_Id']==team_id)]

print(numMatchesPerTeamPerSeason(1,3))

pos=0

for index,row in teamsDF.iterrows():
    team_id=row['Team_Id']
    short_name=row['Team_Short_Code']
    for i,r in seasonsDF.iterrows():
        season_id=r['Season_Id']
        matches=len(numMatchesPerTeamPerSeason(team_id,season_id))
        wins=len(numMatchesWonByTeamInSeason(team_id,season_id))
        win_percent=0
        if (wins>0):
            win_percent=(wins*100)/matches
        new_row=[team_id,short_name, matches, wins, win_percent]
        data.loc[pos]=new_row
        pos=pos+1

print(data)