import pandas
from functools import reduce

ball_by_ball_df = pandas.read_csv('C://Users//Mayank//Desktop//IPL ML//data//Ball_by_Ball1.csv')
match_df = pandas.read_csv('C://Users//Mayank//Desktop//IPL ML//data/Match1.csv')
player_match_df = pandas.read_csv('C://Users//Mayank//Desktop//IPL ML//data/Player_Match1.csv')
player_df = pandas.read_csv('C://Users//Mayank//Desktop//IPL ML//data/Player1.csv')
season_df = pandas.read_csv('C://Users//Mayank//Desktop//IPL ML//data/Season1.csv')
team_df = pandas.read_csv('C://Users//Mayank//Desktop//IPL ML//data/Team1.csv')

com_df1=[match_df, ball_by_ball_df, player_match_df]
df_final1 = reduce(lambda left,right: pandas.merge(left,right,on='Match_Id'), com_df1)
