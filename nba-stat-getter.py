from nba_api.stats.endpoints import playercareerstats, leaguegamefinder
from nba_api.stats.static import teams, players
import pandas as pd

#https://github.com/swar/nba_api

#Business problem
#Want to predict next NBA MVP
#which important variables are we solving for?

#Data collection
#api's from nba_api and possibly scraping another website
#Connect to AWS database and store data

#Data preparation
#Using jupyter notebook
#Load from database
#Clean data
#create features

#Data exploration
#use sns, matplotlib and pandas

#Data Modelling
#split data
#create models

#Model evaluation

#Deployment
#not relevant

career = playercareerstats.PlayerCareerStats(player_id='203999')

df = career.get_data_frames()[0]

nba_teams = pd.DataFrame(data=teams.get_teams())
nba_teams.to_csv('teams.csv')
nba_players = pd.DataFrame(data=players.get_players())
nba_players.to_csv('players.csv')

game_response = leaguegamefinder.LeagueGameFinder()
nba_games = game_response.get_data_frames()[0]
nba_games.to_csv('games.csv')
print(nba_games.info())