import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

topics_dict = json.load(open('data/words_by_topic.json', 'r'))
lda_components = np.load('data/lda_components.npy')
with open('data/topics_description.txt', 'r') as f:
    topics_names = f.read().splitlines() 


def topic_distribution(cluster, lda_components=lda_components, topics_names=topics_names):
    features = ['adjective', 'active verb', 'patient verb']

    cluster_components = lda_components[cluster] / lda_components[cluster].sum()
    top_topics = np.argsort(cluster_components)[-1:-11:-1]
    topic_to_probability = {}
    for i in top_topics:
        feature = features[i // 200]
        topic_to_probability[feature + ': ' + topics_names[i % 200]] = cluster_components[i]
    return topic_to_probability

def plot_topic_distribution(cluster, fig_name=None):
    topic_distr = topic_distribution(cluster, lda_components, topics_names)
    y_pos = np.arange(len(topic_distr))
    fig = plt.figure(figsize=(8, 5))
    plt.barh(y_pos, list(topic_distr.values()))
    plt.yticks(y_pos, labels=list(topic_distr.keys()))
    plt.gca().invert_yaxis()
    plt.xscale('log')
    if fig_name is not None:
        fig.savefig(fig_name, dpi=fig.dpi, bbox_inches='tight')
    else:
        plt.show()
