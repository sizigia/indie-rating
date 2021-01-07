import pandas as pd
import numpy as np
from helpers import get_col_unique_values
import pickle

movies = pd.read_csv('data/movies.csv', index_col='Unnamed: 0')
indie_awards = pickle.load(open('data/awards86_20.pkl', 'rb'))

unique_stars = list(get_col_unique_values(movies, 'stars', char=', '))
unique_directors = list(get_col_unique_values(movies, 'director', char=', '))

awarded_categories = set()

for year in indie_awards.keys():
    for title in indie_awards[year].keys():
        for category in indie_awards[year][title].keys():
            awarded_categories.add(category)

indie_awards_df = pd.DataFrame(columns=['title', 'year', *awarded_categories])

for year in indie_awards.keys():
    row = pd.DataFrame.from_dict(indie_awards[year]).transpose(
    ).reset_index().rename(columns={'index': 'title'})
    row['year'] = year
    indie_awards_df = indie_awards_df.append(
        row, ignore_index=True, verify_integrity=True)

special_distinction_awards = indie_awards_df[indie_awards_df['Special Distinction Award'].notna(
)].dropna(axis=1)

indie_awards_df = indie_awards_df.drop(index=special_distinction_awards.index).drop(
    columns=['Special Distinction Award']).reset_index(drop=True)


def er_identification(row):
    swap_ = ['Abraham Attah', 'Edward Lachman', 'James Laxton',
             'Jarin Blaschke', 'Jean Dujardin', 'Jean-Pierre Jeunet',
             'Jennifer Lawrence', 'Jennifer Todd, Suzanne Todd', 'Rodrigo De la Serna',
             'Sally Kirkland', 'Shailene Woodley', 'Shuzhen Zhao',
             'Tom McCarthy, Josh Singer']

    title = row['title']
    def search_index(string, list_): return list_.index(string)

    if title in unique_stars:
        idx = search_index(title, unique_stars)
        return unique_stars[idx] == title or title != 'Anna'
    elif title in unique_directors:
        idx = search_index(title, unique_directors)
        return unique_directors[idx] == title
    return title in swap_


def er_correction(row):
    vals = row.dropna()

    for col, val in zip(vals.index[::2], vals.values[::-2]):
        indie_awards_df.at[row.name, col] = val


er = indie_awards_df.apply(er_identification, axis=1)
indie_awards_df.loc[er].apply(lambda row: er_correction(row), axis=1)
del er

indie_awards_df = indie_awards_df.groupby(
    by=['title', 'year']).last().reset_index()

indie_awards_df.to_csv(
    "data/indie_awards.csv", index=False)
