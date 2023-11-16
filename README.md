# Cinematic Archetypes: Decoding Societal Preferences
## Abstract: 

In our daily lives, we naturally categorize everything we encounter, including the characters in the movies we love. The characters that capture our collective imagination often mirror our aspirations, fears, and evolving values. This project aims to employ a data-driven approach to cluster movie characters into archetypes. By using these archetypes, we aim to uncover valuable insights into people's preferences for character traits. Using this knowledge, we can not only help filmmakers to create more appealing stories but also look into the prevailing cultural and psychological dynamics in society.

## Research Questions: 
- What character archetypes can we derive, and what methodologies are most effective for this purpose?
- What are the historical trends in preferred archetypes?
- Is there a difference in preferred archetypes based on the country of production? Can we reveal cultural preferences through this analysis?
- Which combinations of archetypes in the film appeal to the audience? How does it depend on the genre of the film?
- Which actors are more successful: those who stick to only one archetype, or those who switch archetypes frequently? Does this change over time? As success metrics, we will use box office revenues and movie ratings.

## Proposed additional datasets: 
[U.S. Bureau of Labor Statistics CPI](https://www.bls.gov/cpi/data.htm) - we will use this dataset to account for inflation and be able to compare the revenues form different years fairly. We can adjust revenues for inflation using the formula $Adjusted Value = \frac{Actual Value}{CPI} \cdot 100$, where $CPI$ is the Consumer Price Index. We are using U.S. CPI (U.S. city average, All items CUUR0000SA0) data since revenue is stated in USD.

[IMDB Movies](https://developer.imdb.com/non-commercial-datasets/) - we will use this dataset to add movie ratings (`averageRating`) to the success measure of films and, possibly, to extract additional data about the actors. We will merge movies by `title`, `runtimeMinutes`, and `startYear` (release year).

## Methods
#### Step 1: Clustering the data
 Clustering is a crucial step in our analysis. We follow the idea suggested in the paper [Learning Latent Personas of Film Characters](https://developer.imdb.com/non-commercial-datasets/) to extract information about character archetypes from the plot text. We implement two methods: Latent Dirichlet Allocation (LDA)-based and BERT-based clustering.

Latent Dirichlet Allocation-based clustering:
- extract linguistic features for each character using spicy
- use word2vec embeddings to cluster these features into topics using Agglomerative Clustering,
- perform Latent Dirichlet Allocation to cluster characters based on their feature topics.
  
BERT-based clustering (refer to `utils/archive/transformer_embeddings.ipynb` for the pipeline):
- obtain the character's embedding from the pre-trained BERT model
- perform clustering (Agglomerative or KMeans) using these embeddings.

We compared our clustering methods with those proposed in the paper. Our methods performed better based on the Variation of Information between learned clusters and between gold clusters extracted from TV Tropes. As the BERT-based method didn't significantly outperform the LDA-based one, we chose LDA for our analysis due to its speed advantage.

After that, we fix the clustering algorithm and search for the best number of clusters for our later analysis using Within-Cluster Sum of Squares.

<!---
###### Interpretability
Latent Dirichlet Allocation can help in interpreting obtained clusters. We can look at the model's components to find the top topics (clusters of words) which can help in understanding which characters' traits are related to being in the particular cluster.
--->

#### Step 2: Archetypes analysis: what trends and patterns could we observe

In this step, we will analyze clusters from the previous step in the following dimensions
- Genre dimension. Do archetypes correspond to the specific genres and how informative are the combinations of archetypes for the definition of the movie genre?
- Time dimension. What time trends could we observe in the archetype distribution?
- Geographical and ethnic dimension. Do the movie languages and countries affect archetype distribution? If so, what cultural patterns could we reveal from archetype preferences?
  - Conduct hypothesis testing to discern variations in preferred archetypes across different countries.
  - Employ Pearson’s Chi-Square test (chi2_contingency from scipy.stats) for statistical analysis.

#### Step 3: Determine the role of different archetypes in the success of the movie
In order to leverage the knowledge of archetypes and determine the role of different archetypes in the success of the movie or the role of the archetypes played by one actor, we need to construct the success metrics for the movie and actors. 

We can use the revenue or IMDB rating to evaluate the movie's success, but it's not that simple for the actor's success. We propose using the weighted average of the revenues/ratings of the movies in which the actor played, with weights proportional to the importance of the role. 
The importance of the role can be evaluated by the number of linguistic features connected to the particular character (which we extracted in the previous step). If the character has a lot of features, they must be an important character.

With this information, we can derive the most successful archetypes from the actor side and analyze them based on time and geographical dimensions as done in the previous step.

#### Step 4: Get the best archetype combination for the movie's success
Linear regression to investigate the impact of specific archetypes on movie success to get insights from the producer side:
 - Fit the model to predict movie revenue/rating based on the archetypes present.
 - Identify statistically significant coefficients, providing insights into the influence of archetypes or their interactions on movie success.

## Proposed timeline
:clock1: 17-11 
- Proof of concept (P2 deadline)
  * Clustering
  * Archetypes analysis by genres
  * Initial analysis of actors' success
  * Initial linear regression model to investigate the impact of specific archetypes on movie success

:clock3: 24-11 
- Movie success evaluation
  * Adjust revenue data for inflation
  * Add ratings to the success metrics
 - Archetype success evaluation
 - Clusters interpretation

:clock5: 01-12
- Analysis of archetypes (step 2)

:clock7: 08-12 
- Finalize answers to the research questions
- Connect findings together to get a story

:clock9: 15-12 
- Clean the code
- Clean the textual description
- Draft Data Story

:clock12: 22-12 
- Final Data Story (P3 deadline)

## Organization within the team: A list of internal milestones up until project Milestone P3.
|        |                           Tasks|
|--------|---------------------------------|
|Jiasheng|Initial data analysis and Step 3 |
|   Edvin|   Step 4 and Data Story         |
|    Rita|          Step 1 and code review |
|   Naoki|Step 4 and assisting in Steps 2&3|
| Mikhail|         Step 2 and Data Story   |
