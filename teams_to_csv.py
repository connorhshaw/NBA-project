from nba_web_scraper import *

all_years = pd.DataFrame()

year_range = range(1990, 1992)

for year in year_range:
    try:
        temp_df = scrape_team_stats(year)
        all_years = pd.concat([all_years, temp_df], ignore_index=True)
    except AttributeError:
        print(f'{year} could not be found.')

    time.sleep(4)

all_years.to_csv('all_teams.csv')