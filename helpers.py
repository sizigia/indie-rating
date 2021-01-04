import re
import numpy as np


def find_movies(movies_to_parse):
    """
    Arguments:
        movies_to_parse: list

    Returns:
        list_of_movies: list
    """
    attrs = ['title', 'year', 'metascore',
             'mpaa_rating', 'runtime_min',
             'genre', 'director', 'stars']

    list_of_movies = []

    for i, _ in enumerate(movies_to_parse):
        attrs_movie = {}
        for attr in attrs:
            attrs_movie[attr] = get_movie_value(movies_to_parse[i], attr)
        list_of_movies.append(attrs_movie)

    return list_of_movies


def get_movie_value(bs4tag, attribute):
    """
    Arguments:
        bs4tag: bs4.element.Tag
        attribute: str

    Returns:
        str or np.nan
    """
    refs = {
        'title': ['a', {'href': re.compile(".+adv_li_tt")}],
        'year': ['span', {'class': 'lister-item-year'}, 'b'],
        'metascore': ['span', {'class': "metascore"}],
        'mpaa_rating': ['span', {'class': 'certificate'}],
        'runtime_min': ['span', {'class': 'runtime'}],
        'genre': ['span', {'class': 'genre'}],
        'director': ['a', {'href': re.compile(".+adv_li_dr.+")}],
        'stars': ['a', {'href': re.compile(".+adv_li_st.+")}]
    }

    if attribute == 'stars':
        tags = bs4tag.find_all(refs[attribute][0], refs[attribute][1])
        return parse_and_format_values(tags, attribute)

    try:
        value = bs4tag.find(refs[attribute][0], refs[attribute][1])
    except:
        value = 0

    if attribute == 'year' and not value:
        try:
            return bs4tag.find(refs[attribute][2]).text
        except AttributeError:
            pass

    if value:
        if attribute in ('title', 'director', 'mpaa_rating'):
            return value.text
        return parse_and_format_values(value, attribute)
    else:
        return np.nan


def parse_and_format_values(value, attribute):
    """
    Arguments:
        value: 
            bs4.element.Tag
            bs4.element.ResultSet
        attribute: str
    Returns:
        formatted value:
            stars: list
            year, metascore, runtime_min: int
            genre: str
    """
    try:
        if attribute == 'stars':
            list_stars = list(map(lambda starstr: starstr.text, value))
            str_stars = ', '.join(list_stars)
            return str_stars

        value = value.text

        if attribute == 'year':
            return re.search('(\d{4})', value).group(1)

        elif attribute == 'metascore':
            return int(value)

        elif attribute == 'runtime_min':
            return int(value[:-3].replace(',', '').replace('.', ''))

        elif attribute == 'genre':
            return value.strip()
    except AttributeError:
        return np.nan


def get_col_unique_values(df, column, char=None):
    """ 
    Arguments:
        df: pandas.DataFrame
        column: str
        char: if type_ is str, then char would be use to split it. Default None.

    Returns:
        set of unique values in the DataFrame column indicated
    """
    unique_values = set()

    for row in df[column]:
        try:
            if row is np.nan:
                pass
            else:
                if char:
                    row = row.split(char)
                else:
                    row = {row}
                unique_values.update(row)
        except AttributeError:
            pass

    return unique_values
