import pandas as pd

def get_imdb_ratings(chunksize=None):
    imdb_rating = pd.read_csv('data/IMDB/ratings.tsv', sep='\t')
    if chunksize is None:
        imdb_titles = pd.read_csv('data/IMDB/titles.tsv', sep='\t', low_memory=False)
    else:
        imdb_titles = next(pd.read_csv('data/IMDB/titles.tsv', sep='\t', low_memory=False, chunksize=chunksize))

    imdb_titles = imdb_titles[(imdb_titles['titleType'] == 'movie')].reset_index(drop=True)
    imdb_titles = imdb_titles[imdb_titles['startYear'].apply(lambda x: x!= '\\N' and int(x) < 2013)]

    title_and_rating = imdb_titles.merge(imdb_rating, left_on='tconst', right_on='tconst')

    title_and_rating['sumRating'] = title_and_rating['averageRating']*title_and_rating['numVotes']
    title_and_rating = title_and_rating.groupby('primaryTitle').agg({'sumRating':'sum', 'numVotes':'sum'}).reset_index()
    title_and_rating['averageRating'] = title_and_rating['sumRating']/title_and_rating['numVotes']

    return title_and_rating[['primaryTitle', 'averageRating']]