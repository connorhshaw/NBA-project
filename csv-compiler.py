from nba_web_scraper import *

# mvp_all_years = pd.DataFrame()
#
# for i in range(1990, 2022):
#     temp_df = scrape_mvp_table(i)
#     mvp_all_years = pd.concat([mvp_all_years, temp_df], ignore_index=True)
#     time.sleep(4)
#
# mvp_all_years.to_csv('mvp-all-years.csv')

teams = ["ATL", "BRK", "BOS","CHO", "CHI", "CLE", "DAL", "DEN", "DET",
         "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL",
         "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC",
         "SAS", "TOR", "UTA", "WAS", "NJN"]

test_teams = ["ATL", "BRK", "BOS"]
test_year_range = range(1990, 1993)

#The following teams codes differ on the website from official NBA team codes
#Brooklyn Nets BRK
#Charlotte CHO
#Phoenix PHO
#Old teams NJN

all_teams = pd.DataFrame()

year_range = range(1990, 2024)
total_progress = len(teams) * len(year_range)
progress_count = 1

for team in teams:
    for year in year_range:
        try:
            temp_df = scrape_team(team, year)
            all_teams = pd.concat([all_teams, temp_df], ignore_index=True)

            print(f'{team} {year} scraped. {progress_count}/{total_progress} complete')
        except AttributeError:
            print(f'{team} {year} could not be found. {progress_count}/{total_progress} complete')
        progress_count += 1

        time.sleep(4)

all_teams.to_csv('all_players.csv')