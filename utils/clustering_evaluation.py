import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from IPython.display import clear_output

from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN
from sklearn import metrics
from sklearn.decomposition import LatentDirichletAllocation

from utils.clustering import get_lda_clusters, get_vocab, word_topics_clustering, sort_meaningful, get_trf_clusters, topic_count

import json
from math import log


def group_labels_by_clusters(clusters):
    _, clusters = np.unique(clusters, return_inverse=True)
    l = [[] for _ in range(np.max(clusters) + 1)]
    for i in range(len(clusters)):
        l[clusters[i]].append(i)
    return l


def variation_of_information(X, Y):
    n = float(sum([len(x) for x in X]))
    sigma = 0.0
    for x in X:
        p = len(x) / n
        for y in Y:
           q = len(y) / n
           r = len(set(x) & set(y)) / n
           if r > 0.0:
               sigma += r * (log(r / p, 2) + log(r / q, 2))
    return abs(sigma)


def same_name(names1, names2):
    names1 = names1.values
    names2 = names2.values
    flag = []
    for i in range(len(names1)):
        flag.append(names2[i] in names1[i])
    return flag

def get_characters_with_tv_trop_info(characters, return_golgen_clusters=True):
    tropes_list=[]
    with open('data/MovieSummaries/tvtropes.clusters.txt', 'r') as f:
        s = f.readline()
        while s:
            trope = s[:s.index('\t')]
            character = json.loads(s[s.index('\t'): ])
            character['trope'] = trope
            tropes_list.append(character)
            s = f.readline()
    topres_df = pd.DataFrame(tropes_list)

    movies = pd.read_csv(
        'data/MovieSummaries/movie.metadata.tsv', 
        sep='\t', 
        names=['wiki_id', 'freebase_id', 'title', 'release_date', 'revenue', 'runtime', 'languages', 'countries', 'genres']
    )
    topres_df = topres_df.merge(movies, how='left', left_on='movie', right_on='title')[['char', 'movie', 'trope', 'wiki_id']]
    tropes_and_clusters = topres_df.merge(characters, how='left', left_on='wiki_id', right_on='wiki_id').dropna()
    tropes_and_clusters = tropes_and_clusters[same_name(tropes_and_clusters['char'], tropes_and_clusters['character'])]
    characters_to_check = tropes_and_clusters.loc[:, tropes_and_clusters.columns != 'char'].reset_index(drop=True)
    if return_golgen_clusters:
        return characters_to_check, group_labels_by_clusters(characters_to_check['trope'].values)
    return characters_to_check


    