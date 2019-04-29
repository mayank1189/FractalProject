# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:57:19 2019

@author: Mayank
"""

import pandas as pd
import numpy as np

from sklearn import preprocessing, svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import V3data as d

pd.set_option('display.max_columns', 30)

teamsDF=pd.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Team.xlsx')
matchesTeamsDF=pd.read_csv('C://Users//Mayank//Desktop//Project-Fractal//Gen1//match_team5.csv')
#matchesTeamsDF['Venue','Team_Id'].corr(matchesTeamsDF['Match_Won'])
data = matchesTeamsDF.drop(['Match_Id'],1)
#data = data.drop(['Unnamed: 0'],1)
data
X = data.drop(['Match_Won'],1)
Y = data['Match_Won']

X = preprocessing.scale(X)
X[16]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.25)

def predict():
    print("Enter Team A Id")
    teamId = input()
    while(len(teamsDF[teamsDF["Team_Id"] == int(teamId)]) == 0):
        print("Please Enter valid Team Id")
        teamId = input()
    print("Enter Team B Id")
    opponentId = input()
    while(len(teamsDF[teamsDF["Team_Id"] == int(opponentId)]) == 0):
        print("Please Enter valid Team Id")
        opponentId = input()
#    print("Enter the venue id")
#    venue=input()
    print("Which team won the toss?Enter Id")
    tossWon = input()
    while((tossWon != teamId) & (tossWon != opponentId)):
        print("Please Enter valid Team Id. %s or %s" % (teamId,opponentId))
        tossWon = input()
    print("Which team bat first?Enter Id")
    batFirst = input()
    while((batFirst != teamId) & (batFirst != opponentId)):
        print("Please Enter valid Team Id. %s or %s" % (teamId,opponentId))
        batFirst = input()
    print ("Enter the venue Id(enter 0mfor neutral)")
    venueId=input()
    print("If it is a day match enter 1 else enter 0?")
    day=input()
    print('@@@@@@@')
    print(d.generatePredictData(int(teamId),int(opponentId),int(tossWon),int(batFirst),int(venueId), int (day)))
    print('@@@@@@@')
    px = d.generatePredictData(int(teamId),int(opponentId),int(tossWon),int(batFirst),int(venueId), int (day))
    
    px = px.drop(['Match_Won'],1)
    px
    px = px.drop(['Match_Id'],1)
    px
    px = preprocessing.scale(px)
    #lin_svm = svm.LinearSVC()
    # print(lin_svm.fit(X_train, y_train))

    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    px
    X_train[0]
    pred = rf.predict(px)
    #pred[0]
    if(pred[0] == 1):
        print("Team A Wins")
    else:
        print("Team B Wins")

def fitModels():

    print("Linear SVM")
    lin_svm = svm.LinearSVC()
    lin_svm.fit(X_train, y_train)
    accu = lin_svm.score(X_test,y_test)
    print(accu)

    print("SVC SVM")
    svc_svm = svm.SVC()
    svc_svm.fit(X_train, y_train)
    accu = svc_svm.score(X_test,y_test)
    print(accu)

    print("Naive Bayes")
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    accu = gnb.score(X_test,y_test)
    print(accu)

    print("Random Forest")
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    accu = rf.score(X_test,y_test)
    print(accu)

fitModels()

predict()


