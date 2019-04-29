# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:03:43 2019

@author: Mayank
"""

import pandas as pd
import numpy as np

bbbsDF = pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Ball_by_Ball.xlsx')
bbbsDF = bbbsDF.convert_objects(convert_numeric=True)
matchesDF = pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Match.xlsx')
playerMatchesDF = pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Player_Match.xlsx')
playersDF = pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Player.xlsx')
seasonsDF = pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Season.xlsx')
teamsDF = pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Team.xlsx')



      
def getMatchesforTeam(team_id):
    return matchesDF[(matchesDF['Team_Name_Id']==team_id) | (matchesDF['Opponent_Team_Id']==team_id)]

def getMatchesWonByTeam(team_id):
    return matchesDF[(matchesDF['Match_Winner_Id']==team_id)]

def getTeamWinPercentage(team_id):
    numberofMatches=len(getMatchesforTeam(team_id))
    numberofMatchesWon=len(getMatchesWonByTeam(team_id))
    win_percent=(numberofMatchesWon*100)/numberofMatches
    return win_percent

def getMatchesforTeamAgainstTeam(team_id,against_id):
#    temp1=len(matchesDF[(matchesDF['Team_Name_Id']==team_id) & (matchesDF['Opponent_Team_Id']==against_id)])
#    temp2=len(matchesDF[(matchesDF['Team_Name_Id']==against_id) & (matchesDF['Opponent_Team_Id']==team_id)])
     return matchesDF[((matchesDF['Team_Name_Id']==team_id) & (matchesDF['Opponent_Team_Id']==against_id)) | ((matchesDF['Team_Name_Id']==against_id) & (matchesDF['Opponent_Team_Id']==team_id))]
    # return matchesDF[((matchesDF["Team_Name_Id"] == team_id) & (matchesDF["Opponent_Team_Id"] == against_id)) | ((matchesDF["Team_Name_Id"] == against_id) & (matchesDF["Opponent_Team_Id"] == team_id))]

def getMatchesWonByTeamAgainstTeam(team_id,against_id):
    totalMatchesDF=matchesDF[((matchesDF['Team_Name_Id']==team_id) & (matchesDF['Opponent_Team_Id']==against_id)) | ((matchesDF['Team_Name_Id']==against_id) & (matchesDF['Opponent_Team_Id']==team_id))]
    return totalMatchesDF[totalMatchesDF['Match_Winner_Id']==team_id]

def getMatchWonPercentageForTeamAgainstTeam(team_id,against_id):
    winPercent=0
    totalMatches=len(getMatchesforTeamAgainstTeam(team_id,against_id))
    totalWins=len(getMatchesWonByTeamAgainstTeam(team_id,against_id))
    if totalWins>0:
        winPercent=(totalWins*100)/totalMatches
    return winPercent

def getMatchWonPercentWhenTossWonForTeam(team_id):
    tossWonDF=len(matchesDF[matchesDF['Toss_Winner_Id']==team_id])
    matchWinTossDF=len(matchesDF[(matchesDF['Toss_Winner_Id']==team_id) & (matchesDF['Match_Winner_Id']==team_id)])
    if tossWonDF > 0:
        tossWinMatchWinPercent= (matchWinTossDF*100)/tossWonDF
    return tossWinMatchWinPercent

    
def getFirstBatWonPercentage(id):
    totalMatchesDF = getMatchesforTeam(id)
    batFirstMatchesDF = totalMatchesDF[((totalMatchesDF["Toss_Winner_Id"]==id) & (totalMatchesDF["Toss_Decision"] == 'bat')) | ((totalMatchesDF["Toss_Winner_Id"]!=id) & (totalMatchesDF["Toss_Decision"] == 'field'))]
    matchesWonDF = batFirstMatchesDF[batFirstMatchesDF["Match_Winner_Id"] == id]
    batFirstMatches = len(batFirstMatchesDF)
    if(batFirstMatches>0):
        matchesWon = len(matchesWonDF)
        return (matchesWon*100)/batFirstMatches
    return 0

def generateWinPercentageSheet():
    data=pd.DataFrame(columns=('team_id', 'opponent_id','win_percent'))
    pos=0
    for index,row in teamsDF.iterrows():
        teamId=row['Team_Id']
        for i,r in teamsDF.iterrows():
            ti=r['Team_Id']
            if(ti!=teamId):
                win_percent=getMatchWonPercentageForTeamAgainstTeam(teamId,ti)
                data.loc[pos,"team_id"]=teamId
                data.loc[pos,"opponent_id"]=ti
                data.loc[pos,"win_percent"]=win_percent
                pos=pos+1
    data.to_csv("C://Users//Mayank//Desktop//Project-Fractal//Gen1//win_percent1.csv", sep=',')
    print("Done")
    
def generatePlayerMatchesCompleteData():
    print("Generating PlayerMatchesComplete Data")
    data = pd.DataFrame(columns=('Match_Id','Player_Id','Team_Id','Batted','Bowls_Played','Runs','Fifties','Hundreds','Out','Bowled','Wickets','Runs_Conceded','Overs','Maiden_Overs','Extras','Wickets_As_Fielder'))
    pos=0
    totalSize=len(playerMatchesDF)
    for index, row in playerMatchesDF.iterrows():
        print("Processing data...( %d %% done)" % int(pos*100/totalSize) )
        runsScored = np.nan
        fifties = np.nan
        hundreds = np.nan
        out = np.nan
        bowlsPlayed = np.nan
        bowled = 0
        batted = 0
        wickets = np.nan
        runsConceded = np.nan
        overs = np.nan
        maidenOvers = np.nan
        extras = np.nan
        matchId=row['Match_Id']
        bbbMatchDF= bbbsDF[bbbsDF['Match_Id']==matchId]
        playerId = row['Player_Id']
        teamId = row["Team_Id"]
        playerAsStrikerDF=bbbMatchDF[bbbMatchDF['Striker_Id']==playerId]
        playerAsBatsmanDF=bbbMatchDF[(bbbMatchDF['Striker_Id']==playerId) | (bbbMatchDF['Non_Striker_Id']==playerId)]
        wicketsAsFielder = len(bbbMatchDF[bbbMatchDF["Fielder_Id"] == playerId])
        if (len(playerAsBatsmanDF)>0):
            batted=1
        if(len(playerAsStrikerDF)>0):
            bowlsPlayed=len(playerAsStrikerDF)
            runsScored=playerAsStrikerDF['Batsman_Scored'].sum()
            out = len(playerAsBatsmanDF[playerAsBatsmanDF["Player_dissimal_Id"] == playerId])
            if (runsScored > 0):
                if(runsScored >= 100):
                    hundreds=(runsScored/100)
                    fifties = int((runsScored - hundreds*100)/50)
                else:
                    hundreds=0
                    fifties=int(runsScored/50)
        playerAsBowlerDF=bbbMatchDF[bbbMatchDF['Bowler_Id']==playerId]
        bowlsThrowed=len(playerAsBowlerDF)
        if(bowlsThrowed > 0):
            bowled=1
            runsConceded=playerAsBowlerDF['Batsman_Scored'].sum()
            wicketsDF=playerAsBowlerDF[playerAsBowlerDF['Player_dissimal_Id']>0]
            wickets=len(wicketsDF)
            extras=playerAsBowlerDF['Extra_Runs'].sum()
            
            
        data.loc[pos,"Match_Id"] = matchId
        data.loc[pos,"Player_Id"] = playerId
        data.loc[pos,"Batted"] = batted
        data.loc[pos,"Bowls_Played"] = bowlsPlayed
        data.loc[pos,"Runs"] = runsScored
        data.loc[pos,"Fifties"] = fifties
        data.loc[pos,"Hundreds"] = hundreds
        data.loc[pos,"Out"] = out
        data.loc[pos,"Bowled"] = bowled
        data.loc[pos,"Wickets"] = wickets
        data.loc[pos,"Runs_Conceded"] = runsConceded
        data.loc[pos,"Overs"] = overs
        data.loc[pos,"Maiden_Overs"] = maidenOvers
        data.loc[pos,"Extras"] = extras
        data.loc[pos,"Team_Id"] = teamId
        data.loc[pos,"Wickets_As_Fielder"] = wicketsAsFielder
        pos = pos + 1
    
    data.to_csv("C:\\Users\\Mayank\\Desktop\\Project-Fractal\\Gen1\\player_match_complete1.csv",sep=',')
    print("Done")

def generateMatchTeamData():
    data = pd.DataFrame(columns=('Match_Id','Team_Id','Opponent_Team_Id','Toss_Won','Bat_First','Win_Percenetage','Opponent_Win_Percentage','Win_Percenetage_Against','Toss_Decision_Win_Percentage','Bat_Decision_Win_Percentage','Match_Won'))
    pos = 0
    for index,row in matchesDF.iterrows():
       #print("Processing data...( %d %% done)" % int(pos*100/totalSize) )
        matchId=row['Match_Id']
        opponentTeamId=row['Opponent_Team_Id']
        teamId=row['Team_Name_Id']
        venue=row['Venue']
        if (venue==''
        teamWinPercentage=getTeamWinPercentage(teamId)
        opponentTeamWinPercentage=getTeamWinPercentage(opponentTeamId)
        teamMatchWinPercentAgainstOpponent=getMatchWonPercentageForTeamAgainstTeam(teamId,opponentTeamId)
        teamTossWon = 0
        opponentTossWon = 0
        teamBatFirst = 0
        opponentBatFirst = 0     
        tossWinTeamId=row['Toss_Winner_Id']
        batDecision=row['Toss_Decision']
        teamTossDescionWinPercentage = getMatchWonPercentWhenTossWonForTeam(teamId)
        opponentTeamTossDescionWinPercentage = getMatchWonPercentWhenTossWonForTeam(opponentTeamId)
        teamBatDecisionWonPercentage = getFirstBatWonPercentage(teamId)
        opponentBatDecisionWonPercentage = getFirstBatWonPercentage(opponentTeamId)
        if(tossWinTeamId==teamId):
            #Toss won by TeamID 
            teamTossWon=1
            opponentTeamTossDescionWinPercentage=100-opponentTeamTossDescionWinPercentage
            if(batDecision=='bat'):
                # Toss Wonby Team ID and chose to Bowl
                teamBatFirst=1
                opponentBatDecisionWonPercentage=100-opponentBatDecisionWonPercentage
            else:
                #Toss Won by Team ID and chose to field
                opponentBatFirst=1
                teamBatDecisionWonPercentage=100-teamBatDecisionWonPercentage
        else:
            #Toss won by Opponent Team
            opponentTossWon=1
            teamTossDescionWinPercentage=100-teamTossDescionWinPercentage
            if(batDecision=='bat'):
                #Toss won by opponent team and chose to bat
                opponentBatFirst=1
                teamBatDecisionWonPercentage=100-teamBatDecisionWonPercentage           
            else:
                ##Toss won by Opponent and chose to bowl
                teamBatFirst=1
                opponentBatDecisionWonPercentage=100-opponentBatDecisionWonPercentage
        matchWon=row['Match_Winner_Id']
        teamMatchWon=0
        opponentMatchWon=0
        if(matchWon==teamMatchWon):
            teamMatchWon=1
        else:
            opponentMatchWon=1
        data.loc[pos,"Match_Id"] = matchId
        data.loc[pos,"Team_Id"] = teamId
        data.loc[pos,"Toss_Won"] = teamTossWon
        data.loc[pos,"Bat_First"] = teamBatFirst
        data.loc[pos,"Win_Percenetage"] = teamWinPercentage
        data.loc[pos,"Opponent_Win_Percentage"] = opponentTeamWinPercentage
        data.loc[pos,"Win_Percenetage_Against"] = teamMatchWinPercentAgainstOpponent
        data.loc[pos,"Toss_Decision_Win_Percentage"] = teamTossDescionWinPercentage
        data.loc[pos,"Bat_Decision_Win_Percentage"] = teamBatDecisionWonPercentage
        data.loc[pos,"Match_Won"] = teamMatchWon
        pos = pos + 1
        
        data.loc[pos,"Match_Id"] = matchId
        data.loc[pos,"Team_Id"] = opponentTeamId
        data.loc[pos,"Toss_Won"] = opponentTossWon
        data.loc[pos,"Bat_First"] = opponentBatFirst
        data.loc[pos,"Win_Percenetage"] = opponentTeamWinPercentage
        data.loc[pos,"Opponent_Win_Percentage"] = teamWinPercentage
        data.loc[pos,"Win_Percenetage_Against"] = 100 - teamMatchWinPercentAgainstOpponent
        data.loc[pos,"Toss_Decision_Win_Percentage"] = opponentTeamTossDescionWinPercentage
        data.loc[pos,"Bat_Decision_Win_Percentage"] = opponentBatDecisionWonPercentage
        data.loc[pos,"Match_Won"] = opponentMatchWon
        pos = pos + 1
    
    data.to_csv("C:\\Users\\Mayank\\Desktop\\Project-Fractal\\Gen1\\match_team1.csv",sep=',')
    print("Done")
    
def calculateBatsmanScore(row):
    PAR_AVG=122.84
    score=0
    runs=row['Runs']
    fifties=row['Fifties']
    hundreds=row['Hundreds']
    bowlsPlayed=row['Bowls_Played']
    out=row['Out']
    average=0
    if(bowlsPlayed>0):
        average = (runs*100)/bowlsPlayed
    wicketsAsFielder = row["Wickets_As_Fielder"]
    if(runs > 0):
        score = score + runs
        score = score + fifties*25
        score = score + hundreds*50
        if(out == 0):
            score = score + 10
        relative_avg = average/PAR_AVG
        score = score*relative_avg
    else:
        if(out == 1):
            score = score - 15
    if(wicketsAsFielder > 0):
        score = score + 10*wicketsAsFielder
    return score

def calculateBowlerScore(row):
    score = 0
    wickets = row["Wickets"]
    runsConceded = row["Runs_Conceded"]
    economy = 0
    extras = row["Extras"]
    overs = row["Overs"]
    maidenOvers = row["Maiden_Overs"]
    wicketsAsFielder = row["Wickets_As_Fielder"]
    if(overs>0):
        economy = runsConceded/overs
    if(wickets > 0):
        score = score + 22.5*wickets
        if(wickets >= 4 ):
            score = score + 10*wickets
    if(extras >= 10):
        score = score - 10
    elif(extras >= 5):
        score = score - 5
    elif(extras > 0):
        score = score -2
    if(maidenOvers > 0):
        score = score + maidenOvers*10
    if(wicketsAsFielder > 0):
        score = score + 10*wicketsAsFielder
    return score

def generatePlayerMatchScoreData():
    playersMatchesCompleteDF = pd.read_csv("C:\\Users\\Mayank\\Desktop\\Project-Fractal\\Gen1\\player_match_complete1.csv")
    playersMatchesCompleteDF = playersMatchesCompleteDF.convert_objects(convert_numeric=True)
    print("Generating PlayerMatchesComplete Data")
    data = pd.DataFrame(columns=('Match_Id','Player_Id','Team_Id','Is_Batsman','Is_Bowler','Is_Allrounder','Score'))
    pos = 0
    totalSize = len(playersMatchesCompleteDF)
    for index,row in playersMatchesCompleteDF.iterrows():
        print("Processing data...( %d %% done)" % int(pos*100/totalSize) )
        isBatsman = 0
        isBowler = 0
        isAllRounder = 0
        score = 0
        matchId = row["Match_Id"]
        playerId = row['Player_Id']
        teamId = row["Team_Id"]
        playerMatchesCompleteDF = playersMatchesCompleteDF[(playersMatchesCompleteDF["Player_Id"] == playerId)]
        totalMatches = len(playerMatchesCompleteDF)
        battedMatchedDF = playerMatchesCompleteDF[playerMatchesCompleteDF["Batted"] == 1]
        bowledMatchesDF = playerMatchesCompleteDF[playerMatchesCompleteDF["Bowled"] == 1]
        bothMatchesDF = playerMatchesCompleteDF[(playerMatchesCompleteDF["Batted"] == 1)&(playerMatchesCompleteDF["Bowled"] == 1)]
        battedMatches = len(battedMatchedDF)
        bowledMatches = len(bowledMatchesDF)
        bothMatches = len(bothMatchesDF)
        if(((bothMatches*100)/totalMatches) > 66):
            isAllRounder = 1
            isBatsman = 0
            isBowler = 0
            score = calculateBatsmanScore(row) + calculateBowlerScore(row)
        elif(battedMatches > bowledMatches):
            isBatsman = 1
            isAllRounder = 0
            isBowler = 0
            score = calculateBatsmanScore(row)
        else:
            isBowler = 1
            isBatsman = 0
            isAllRounder = 0
            score = calculateBowlerScore(row)
        data.loc[pos,'Match_Id'] = matchId
        data.loc[pos,'Player_Id'] = playerId
        data.loc[pos,"Team_Id"] = teamId
        data.loc[pos,'Is_Batsman'] = isBatsman
        data.loc[pos,'Is_Bowler'] = isBowler
        data.loc[pos,'Is_Allrounder'] = isAllRounder
        data.loc[pos,'Score'] = score
        pos = pos + 1
    data.to_csv("C:\\Users\\Mayank\\Desktop\\Project-Fractal\\Gen1\\player_match_score1.csv",sep=',')
    print("Done")
    
def generatePlayerScoreData():
    print("Generating PlayerScore Data")
    data = pd.DataFrame(columns=('Player_Id','Player_Name','Total_Score','Avg_Score'))
    playersMatchesScoreDF = pd.read_csv("C:\\Users\\Mayank\\Desktop\\Project-Fractal\\Gen1\\player_match_score1.csv")
    pos = 0
    for index,row in playersDF.iterrows():
        score = 0
        totalScore = 0
        playerId = row["Player_Id"]
        name = row["Player_Name"]
        playerMatchesDF = playersMatchesScoreDF[playersMatchesScoreDF["Player_Id"] == playerId]
        totalMatches = len(playerMatchesDF)
        if(totalMatches>0):
            totalScore = playerMatchesDF["Score"].sum()
            score = totalScore/totalMatches
        data.loc[pos,"Player_Id"] = playerId
        data.loc[pos,"Player_Name"] = name
        data.loc[pos,"Total_Score"] = totalScore
        data.loc[pos,"Avg_Score"] = score
        pos = pos + 1
    data.to_csv("C:\\Users\\Mayank\\Desktop\\Project-Fractal\\Gen1\\player_score1.csv",sep=',')
    print("Done")
    
def generatePredictData(teamId,opponentId,tossWon,batFirst, day):    
    data = pd.DataFrame(columns=('Match_Id','Team_Id','Day','Toss_Won','Bat_First','Win_Percenetage','Opponent_Win_Percentage','Win_Percenetage_Against','Toss_Decision_Win_Percentage','Bat_Decision_Win_Percentage','Match_Won'))
    data
    pos = 0
    matchId = 1
    teamTossWon = 0
    teamBatFirst = 0
    teamWinPercentage = getTeamWinPercentage(teamId)
    opponentTeamWinPercentage = getTeamWinPercentage(opponentId)
    teamMatchWinPercentAgainstOpponent = getMatchWonPercentageForTeamAgainstTeam(teamId,opponentId)
    teamTossDescionWinPercentage = getMatchWonPercentWhenTossWonForTeam(teamId)
    teamBatDecisionWonPercentage = getFirstBatWonPercentage(teamId)
    if(tossWon == teamId):
        teamTossWon = 1
    else:
        teamTossDescionWinPercentage = 100 - teamTossDescionWinPercentage
    
    if(batFirst == teamId):
        teamBatFirst = 1
    else:
        teamBatDecisionWonPercentage = 100 - teamBatDecisionWonPercentage
    data.loc[pos,"Match_Id"] = matchId
    data.loc[pos,"Team_Id"] = teamId
    data.loc[pos,"Day"] = day
    data.loc[pos,"Toss_Won"] = teamTossWon
    data.loc[pos,"Bat_First"] = teamBatFirst
    data.loc[pos,"Win_Percenetage"] = teamWinPercentage
    data.loc[pos,"Opponent_Win_Percentage"] = opponentTeamWinPercentage
    data.loc[pos,"Win_Percenetage_Against"] = teamMatchWinPercentAgainstOpponent
    data.loc[pos,"Toss_Decision_Win_Percentage"] = teamTossDescionWinPercentage
    data.loc[pos,"Bat_Decision_Win_Percentage"] = teamBatDecisionWonPercentage
    data.loc[pos,"Match_Won"] = 0
    print(data)
    return data


# generateWinPercentageSheet()
#generatePlayerMatchesCompleteData()
#generateMatchTeamData()
#generatePlayerMatchScoreData()
generatePredictData(1,2,1,1,1)