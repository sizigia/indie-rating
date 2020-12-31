import chromedriver_autoinstaller
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helpers import find_movies, get_movie_value

# Check if the current version of chromedriver exists
chromedriver_autoinstaller.install()

# Driver:
options = Options()
options.page_load_strategy = 'normal'  # 'eager', 'none'

driver = webdriver.Chrome()


# create dataframe to append results
cols = ['title',
        'year',
        'metascore',
        'mpaa_rating',
        'runtime_min',
        'genre',
        'director',
        'stars']
df = pd.DataFrame(columns=cols)

# set up first link to check for movies
imdb_query = 'https://www.imdb.com/search/title/?keywords=independent-film&sort=release_date,desc'
driver.get(imdb_query)


def update_df(df, soup):
    movie_list = soup.find_all('div', {'class': "lister-item-content"})
    list_of_movies = find_movies(movie_list)
    df = df.append(pd.DataFrame(list_of_movies), ignore_index=True)
    df.to_csv('data/movies.csv')
    return df


# loop through
try:
    while driver.find_element_by_class_name("next-page"):
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        df = update_df(df, soup)

        nxt = driver.find_element_by_class_name("next-page")
        nxt.click()
        driver.get(driver.current_url)
except:
    driver.get(driver.current_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    df = update_df(df, soup)

# close driver
driver.quit()
