import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from utils.transformer_character_embeddings import embeddings_from_text
from utils.character_attributes_extraction import attributes2vec, word2vec

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import AgglomerativeClustering, KMeans


def get_transformer_embeddings(plots_with_cluster_labels, save_to=None):
    character_list = []

    for index, row in tqdm([row for row in plots_with_cluster_labels.iterrows()]):
        plot = row["plot"]
        character_emb = embeddings_from_text(plot)

        for name in character_emb.keys():
            character_list.append(
                {
                    "wiki_id": row["wiki_id"],
                    "character": name,
                    "emb": character_emb[name].tolist(),
                }
            )

    character_df = pd.DataFrame(character_list)
    if save_to:
        character_df.to_csv("data/" + save_to)
    return character_df

def get_trf_clusters(characters, algo):
    X = np.array(characters['emb'].values.tolist())
    clustering = algo.fit(X)
    return clustering.labels_


def sort_meaningful(characters, min_attr_length):
    def len_attr(x):
        a = 0
        for w in x["adj"]:
            a += w.isalpha()
        for w in x["active"]:
            a += w.isalpha()
        for w in x["patient"]:
            a += w.isalpha()
        return a

    return (
        characters[characters.apply(len_attr, axis=1) >= min_attr_length]
        .reset_index(drop=True)
        .copy()
    )


def get_vocab(characters, min_freq, max_freq):
    vocab = (
        [w.lower() for i, r in characters.iterrows() for w in r["adj"] if w.isalpha()]
        + [
            w.lower()
            for i, r in characters.iterrows()
            for w in r["active"]
            if w.isalpha()
        ]
        + [
            w.lower()
            for i, r in characters.iterrows()
            for w in r["patient"]
            if w.isalpha()
        ]
    )
    vocab, vocab_count = np.unique(vocab, return_counts=True)
    
    # we use relative max_freq
    max_freq = int(max_freq * len(vocab))

    vocab = vocab[np.logical_and(vocab_count >= min_freq, vocab_count <= max_freq)]
    vocab_vectors = [word2vec(w).tolist() for w in vocab.tolist()]
    return vocab, np.array(vocab_vectors) + 1e-9


def word_topics_clustering(vocab, vocab_vectors, clustering_algo):
    clustering = clustering_algo.fit(vocab_vectors)
    labels = clustering.labels_

    topic_dict = {}
    for i in tqdm(range(len(vocab))):
        topic_dict[vocab[i]] = labels[i]
    return topic_dict


def topic_count(characters, topic_dict):
    num_topics = max(topic_dict.values()) + 1
    attr_topic_count = np.zeros((len(characters), num_topics * 3))
    for i, r in tqdm(characters.iterrows(), total=characters.shape[0]):
        for w in r["adj"]:
            if w in topic_dict:
                j = topic_dict[w]
                attr_topic_count[i][j] += 1
        for w in r["active"]:
            if w in topic_dict:
                j = topic_dict[w]
                attr_topic_count[i][num_topics + j] += 1
        for w in r["patient"]:
            if w in topic_dict:
                j = topic_dict[w]
                attr_topic_count[i][2 * num_topics + j] += 1
    return attr_topic_count


def get_topic_counts(characters, min_freq, max_freq, clustering_algo):
    print('vocabulary extraction')
    vocab, vocab_vectors = get_vocab(characters, min_freq, max_freq)
    print('vocabulary extraction DONE')
    print('topics clustering')
    topic_dict = word_topics_clustering(vocab, vocab_vectors, clustering_algo)
    print('topics clustering DONE')
    print('topics count')
    counts = topic_count(characters, topic_dict)
    print('topics count DONE')
    return counts


def lda_clustering(topic_count, n_components, random_state=0):
    lda = LatentDirichletAllocation(
        n_components=n_components, random_state=random_state
    ).fit_transform(topic_count)
    return lda.argmax(axis=1)

def kmeans_clustering(topic_count, n_components, random_state=0):
    kmeans = KMeans(
        n_clusters=n_components, random_state=random_state
    ).fit_predict(topic_count)
    return kmeans

def get_lda_clusters(
    characters, min_freq, max_freq, clustering_algo, n_components, return_topic_counts=False
):
    topic_count = get_topic_counts(
        characters, min_freq, max_freq, clustering_algo
    )
    print('LDA')
    if return_topic_counts:
        return lda_clustering(topic_count, n_components), topic_count
    return lda_clustering(topic_count, n_components)


def get_kmeans_clusters(
    characters, min_freq, max_freq, clustering_algo, n_components
):
    topic_count = get_topic_counts(
        characters, min_freq, max_freq, clustering_algo
    )
    print('KMeans')
    return kmeans_clustering(topic_count, n_components)
