# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:48:01 2019

@author: Mayank
"""

import pandas

ball_by_ball_df = pandas.read_excel("C://Users//Mayank//Desktop//Project-Fractal//data//Ball_By_Ball.xlsx")

match_df = pandas.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Match.xlsx')
player_match_df = pandas.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Player_Match.xlsx')
player_df = pandas.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Player.xlsx')
season_df = pandas.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Season.xlsx')
team_df = pandas.read_excel('C://Users//Mayank//Desktop//Project-Fractal//data//Team.xlsx')

#com_df1=[match_df, ball_by_ball_df, player_match_df]
#df_final1 = reduce(lambda left,right: pandas.merge(left,right,on='Match_Id'), com_df1)
#
##com_df2=[df_final1,season_df]
##df_final2=reduce(lambda left,right: pandas.merge(left,right,left_on='Season_Id_x', right_on='Season_Id'), com_df2)
#df_final2=pandas.merge(df_final1,season_df,left_on='Season_Id_x', right_on='Season_Id')
#
##com_df3=[com_df2, player_df]
#df_final3=pandas.merge(df_final2,player_df,on='Player_Id')
#
##com_df_final=[com_df3, team_df]
#df_final_full=pandas.merge(df_final3,team_df, on='Team_Id')
#
#export_csv = df_final_full.to_csv (r'C://Users//Mayank//Desktop//Project-Fractal//FullData1.csv', index = None, header=True, sep=',') #Don't forget to add '.csv' at the end of the path