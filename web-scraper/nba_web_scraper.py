import requests
import bs4 as bs
import pandas as pd
import time

#cleaning
#MVP data
#all player data
#team success (seed or wins)

#cleaning
#filter all player data
#MVP share
#join all data to one table

#import mysql.connector
import sys
import boto3
import os

# ENDPOINT="mysqldb.123456789012.us-east-1.rds.amazonaws.com"
# PORT="3306"
# USER="jane_doe"
# REGION="us-east-1"
# DBNAME="mydb"
# os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#we will block users sending requests to our sites more often than twenty requests in a minute

def scrape_mvp_table(year):

    website = f'https://www.basketball-reference.com/awards/awards_{year}.html'

    response = requests.get(url=website)
    print(response)
    if response.status_code == 429:
        print(response.headers["Retry-After"])
    page_data = response.text
    soup = bs.BeautifulSoup(page_data, 'html.parser')

    mvp_table = soup.find(id="div_mvp")
    #print(mvp_table.prettify())
    row_elements = mvp_table.findAll("tr")
    row_elements.pop(0)
    row_elements.pop(0)

    header_list=[]

    for header_element in row_elements[1]:
        header_list.append(header_element["data-stat"])

    mvp_stats = pd.DataFrame(columns=header_list)

    for row_element in row_elements:
        player_dict = {}
        for player_attr in row_element.findAll(['th', 'td']):
            player_dict[player_attr["data-stat"]]=player_attr.text

        if len(player_dict) > 0 and not player_dict.get("player") == "Player":
            player_df = pd.DataFrame(player_dict, columns=header_list, index=[0])
            mvp_stats = pd.concat([mvp_stats, player_df], ignore_index=True)

    mvp_stats['Year'] = year
    return mvp_stats

def scrape_team(team, year):
    website = f'https://www.basketball-reference.com/teams/{team}/{year}.html'

    response = requests.get(url=website)
    print(response)
    if response.status_code == 429:
        print(response.headers["Retry-After"])
    page_data = response.text
    soup = bs.BeautifulSoup(page_data, 'html.parser')

    avg_table = soup.find(id="div_per_game")
    avg_row_elements = avg_table.findAll("tr")
    avg_row_elements.pop(0)

    adv_table = soup.find(id="div_advanced")
    adv_row_elements = adv_table.findAll("tr")
    adv_row_elements.pop(0)

    header_list = []

    for header_element in avg_row_elements[1]:
        header_list.append(header_element["data-stat"])

    for header_element in adv_row_elements[1]:
        header_list.append(header_element["data-stat"])

    #print(header_list)

    team_stats = pd.DataFrame(columns=header_list)

    for avg_row_element, adv_row_element in zip(avg_row_elements, adv_row_elements):
        player_dict = {}
        for player_attr in avg_row_element.findAll(['th', 'td']):
            player_dict[player_attr["data-stat"]]=player_attr.text

        for player_attr in adv_row_element.findAll(['th', 'td']):
            player_dict[player_attr["data-stat"]]=player_attr.text

        if len(player_dict) > 0 and not player_dict.get("player") == "Player":
            player_df = pd.DataFrame(player_dict, columns=header_list, index=[0])
            team_stats = pd.concat([team_stats, player_df], ignore_index=True)

    team_stats['Team'] = team
    team_stats['Year'] = year
    return team_stats


def scrape_year(year):
    website_adv = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'
    website_avg = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'

    response_avg = requests.get(url=website_avg)
    print(response_avg)
    if response_avg.status_code == 429:
        print(response_avg.headers["Retry-After"])
    page_data_avg = response_avg.text
    soup_avg = bs.BeautifulSoup(page_data_avg, 'html.parser')
    #print(soup_avg)

    time.sleep(4)
    response_adv = requests.get(url=website_adv)
    print(response_adv)
    if response_adv.status_code == 429:
        print(response_adv.headers["Retry-After"])
    page_data_adv = response_adv.text
    soup_adv = bs.BeautifulSoup(page_data_adv, 'html.parser')

    avg_table = soup_avg.find(id="per_game_stats")
    avg_row_elements = avg_table.findAll("tr")
    avg_row_elements.pop(0)

    adv_table = soup_adv.find(id="advanced_stats")
    adv_row_elements = adv_table.findAll("tr")
    adv_row_elements.pop(0)

    header_list = []

    for header_element in avg_row_elements[1]:
        header_list.append(header_element["data-stat"])

    for header_element in adv_row_elements[1]:
        header_list.append(header_element["data-stat"])

    team_stats = pd.DataFrame(columns=header_list)

    for avg_row_element, adv_row_element in zip(avg_row_elements, adv_row_elements):
        player_dict = {}
        for player_attr in avg_row_element.findAll(['th', 'td']):
            player_dict[player_attr["data-stat"]]=player_attr.text

        for player_attr in adv_row_element.findAll(['th', 'td']):
            player_dict[player_attr["data-stat"]]=player_attr.text

        if len(player_dict) > 0 and not player_dict.get("player") == "Player":
            player_df = pd.DataFrame(player_dict, columns=header_list, index=[0])
            team_stats = pd.concat([team_stats, player_df], ignore_index=True)

    team_stats['Year'] = year
    return team_stats

def scrape_team_stats(year):

    website = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'

    response = requests.get(url=website)
    print(response)
    if response.status_code == 429:
        print(response.headers["Retry-After"])
    page_data = response.text
    soup = bs.BeautifulSoup(page_data, 'html.parser')

    if soup.findAll(id="confs_standings_E") == []:
        east_table = soup.find(id="divs_standings_E")
    else:
        east_table = soup.find(id="confs_standings_E")
    row_elements_east = east_table.findAll("tr")
    row_elements_east.pop(0)
    row_elements_east.pop(0)

    print(row_elements_east)

    if soup.findAll(id="confs_standings_W") == []:
        west_table = soup.find(id="divs_standings_W")
    else:
        west_table = soup.find(id="confs_standings_W")
    row_elements_west = west_table.findAll("tr")
    row_elements_west.pop(0)
    row_elements_west.pop(0)

    print(row_elements_west)

    header_list=[]

    for header_element in row_elements_east[1]:
        header_list.append(header_element["data-stat"])

    team_stats = pd.DataFrame(columns=header_list)

    print(team_stats)

    for row_element in row_elements_east:
        team_dict = {}
        for team_attr in row_element.findAll(['td', 'th']):
            if team_attr
            team_dict[team_attr["data-stat"]]=team_attr.text

        if len(team_dict) > 0:
            team_df = pd.DataFrame(team_dict, columns=header_list, index=[0])
            team_stats = pd.concat([team_stats, team_df], ignore_index=True)
            print(team_stats)

    for row_element in row_elements_west:
        team_dict = {}
        for team_attr in row_element.findAll(['td', 'th']):
            team_dict[team_attr["data-stat"]]=team_attr.text

        if len(team_dict) > 0:
            team_df = pd.DataFrame(team_dict, columns=header_list, index=[0])
            team_stats = pd.concat([team_stats, team_df], ignore_index=True)

    team_stats['Year'] = year

    return team_stats