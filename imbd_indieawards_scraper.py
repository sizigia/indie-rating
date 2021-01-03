import chromedriver_autoinstaller
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Check if the current version of chromedriver exists
chromedriver_autoinstaller.install()

# Driver:
options = Options()
options.page_load_strategy = 'normal'  # 'eager', 'none'

driver = webdriver.Chrome()


# create variables to store results
y_awards = {}

# set up first link to check for movies
imdb_yr_query = 'https://www.imdb.com/event/ev0000349/{}/1/?ref_=ev_eh'
years_to_scrape = range(1986, 2021)


# loop through
for year in years_to_scrape:
    awards = {}
    url_ = imdb_yr_query.format(year)

    driver.get(url_)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    awards_list = soup.find_all('div', {'class': 'event-widgets__award'})

    for award_ in awards_list:
        categories = award_.find_all(
            'div', {'class': 'event-widgets__award-category'})
        award_name = award_.find(
            'div', {'class': 'event-widgets__award-name'}).text

        for idx, category in enumerate(categories):
            try:
                if award_name == 'Special Distinction Award':
                    cat_name = 'Special Distinction Award'
                else:
                    cat_name = category.find(
                        'div', {'class': 'event-widgets__award-category-name'}).text
                nominations_div = category.find(
                    'div', {'class': "event-widgets__award-category-nominations"})
                nomination_rows = nominations_div.find_all(
                    'div', {'class': "event-widgets__award-category-nominations-row"})

                for row in nomination_rows:
                    noms = row.find_all(
                        'div', {'class': "event-widgets__award-nomination"})

                    for nom in noms:
                        if nom.find(
                                'div', {'class': "event-widgets__winner-badge"}):
                            movie = nom.find(
                                'div', {'class': "event-widgets__primary-nominees"}).text

                            rep = nom.find(
                                'div', {'class': "event-widgets__secondary-nominees"}).text

                            if cat_name in ['Best Director']:
                                if rep not in awards.keys():
                                    awards[rep] = {}
                            elif movie not in awards.keys():
                                awards[movie] = {}

                            if cat_name in ['Best Director']:
                                awards[rep][cat_name] = movie
                            else:
                                awards[movie][cat_name] = rep or '-'
            except:
                pass

    y_awards[year] = awards
    # save results to file
    pickle.dump(y_awards, open('data/awards86_20.pkl', 'wb'))

# close driver
driver.quit()
