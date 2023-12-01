import pandas as pd

def get_imdb_ratings(imdb_titles, movies):
    imdb_rating = pd.read_csv('data/IMDB/ratings.tsv', sep='\t')

    imdb_titles = imdb_titles[(imdb_titles['titleType'] == 'movie')].reset_index(drop=True)
    imdb_titles = imdb_titles[imdb_titles['startYear'].apply(lambda x: x!= '\\N' and int(x) < 2013)]

    title_and_rating = imdb_titles.merge(imdb_rating, left_on='tconst', right_on='tconst')[['primaryTitle', 'startYear', 'averageRating', 'numVotes']]
    title_and_rating = title_and_rating.merge(movies, left_on=['primaryTitle', 'startYear'], right_on=['title', 'release_year'])

    return title_and_rating

def movies_with_imdb_rating(movies):
    def release_year(x):
        if type(x) is str:
            return x.split('-')[0]
        else:
            return x

    movies['release_year'] = movies['release_date'].apply(release_year)
    
    chunksize = 1000000

    list_of_dfs = []
    for df in pd.read_csv('data/IMDB/titles.tsv', sep='\t', low_memory=False, chunksize=chunksize):
        title_and_rating = get_imdb_ratings(df, movies)
        list_of_dfs.append(title_and_rating)
    return pd.concat(list_of_dfs)