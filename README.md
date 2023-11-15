# Title
## Abstract: 

In our daily lives, we naturally categorize everything we encounter, including the characters in the movies we love. The goal of this project is to employ a data-driven approach to find clusters of movie characters or archetypes. By using these archetypes, we aim to uncover valuable insights into people's preferences for character traits. Using this knowledge, we can not only help filmmakers to create more appealing stories, but also look into the prevailing cultural and psychological dynamics in the society.

## Research Questions: 
- Which actors are more succesfull: those who stick to only one archetype, or those who switch archetypes frequently?
- Which combinations of archetypes in the film appeal to the audience? How does it depend on the genre of the film?
- Is there a difference in preferred archetypes based on the country of production?
- What are the historical trends in preferred archetypes?

## Proposed additional datasets: 
[World Bank CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2012&start=1990&view=chart) - we will use this dataset to account for inflation and be able to fairly compare the revenues form different years.

[IMDB Movies](https://developer.imdb.com/non-commercial-datasets/) - we will use this dataset to add movies rating to the succes measure of the film and possibly to extracting additional data about the actors.

## Methods
#### Step 1: Clustering the data
 Clustering is a crucial step in our analysis. We follow the idea suggested in the paper [Learning Latent Personas of Film Characters](https://developer.imdb.com/non-commercial-datasets/) to extrat information about character archetypes from the plot text. We implemet two methods: Latent Dirichlet Allocation (LDA)-based and BERT-based.

Latent Dirichlet Allocation-based clustering:
- extract linguistic features for each character (attributes, active and patient verbs),
- use word2vec embeddings to cluster this features into topics using Agglomerative Clustering,
- perform Latent Dirichlet Allocation to cluster characters based of their features topics.
  
BERT-based clustering:
- obtain character's embedding as the mean of the pretrained BERT embeddings of character's name tokens in the text of the plot,
- performe clustering (Agglomerative or KMeans) using this embeddings.

Then we compare the quality of our clustering methods with the quality of the clustering proposed in the paper "Learning Latent Personas of Film Characters". The performance of our clustering methods is better when comparing Variation of Information between learned clusters and gold clusters extracted from TV Tropes ([refer](http://www.cs.cmu.edu/~dbamman/pubs/pdf/bamman+oconnor+smith.acl13.pdf) to the paper for the details). And since the performane of BERT-based method is not much better than the performance of LDA-based method, we will use LDA-based clustering for our analysis, since it's faster.

After that, we fix the clustering algorithm and search for the best number of cluster for our later analysis using Silhouette Coefficient.

#### Step 2: Evaluating success
In order to leverage the knowledge of archetypes and determine the role of different archetypes in the succes of the movie or the role of the archetypes played by one actor, we need to construct the success metrics for the movie and actors. We can use the revenue or IMDB rating to ecaluate the movie success, but it's not that simple for the actor's succes. We propose using the weighted average of the revenues/rating of the movies in which the actor played, whith weights proportional to the importance of the role. Importance of the role can be evaluated by the number of linguistic features connected to the particular character (which we extracted in the previous step). If the character has a lot of features, they must be an important character.

#### Step 3: Answering research questions


## Proposed timeline
17-11 
- Proof of concept (P2 deadline)
 * Clustering
 * Initial analysis of actors' success
 * Archetypes distribuion by actors' age and sex
 * Achetypes distribution by genres

24-11 
- Final success evaluation
 * Adjust revenue data for inflation
 * Add ratings to the success metrics
- Basic analysis of archetypes
 * Geographycal trends in archetypes
 * Historical trends in archetypes

01-12
- Answer the research questions

08-12 
- Clean the code
- Clean the textual description

15-12 
- Draft Data Story

22-12 
- Final Data Story (P3 deadline)

## Organization within the team: A list of internal milestones up until project Milestone P3.
|        |                           Tasks|
|--------|--------------------------------|
|Jiasheng|Initial actor's success analysis|
|   Edvin|                                |
|    Rita|                      Clustering|
|   Naoki|                                |
| Mikhail|                                |

## Questions for TAs (optional): Add here any questions you have for us related to the proposed project.

