# Title
## Abstract: 

In our daily lives, we naturally categorize everything we encounter, including the characters in the movies we love. The goal of this project is to employ a data-driven approach to find clusters of movie characters or archetypes. By using these archetypes, we aim to uncover valuable insights into people's preferences for character traits. Using this knowledge, we can not only help filmmakers to create more appealing stories, but also look into the prevailing cultural and psychological dynamics in the society.

## Research Questions: 
- Which actors are more succesfull: those who stick to only one archetype, or those who switch archetypes frequently?
- Which combinations of archetypes in the film appeal to the audience? How does it depend on the genre of the film?
- Is there a difference in prefered archetypes based on the country of production?
- What are the historical trends in preffered archetypes?

## Proposed additional datasets: 
[World Bank CPI](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2012&start=1990&view=chart) - we will use this dataset to account for inflation and be able to fairly compare the revenues form different years
[IMDB Movies](https://developer.imdb.com/non-commercial-datasets/) - we will use this dataset to add movies rating to the succes measure of the film and possibly to extracting additional data about the actors.

## Methods
1) Clustering the data
 Clustering is a crucial step in our analysis. We follow the idea suggested in the paper [Learning Latent Personas of Film Characters](https://developer.imdb.com/non-commercial-datasets/) to extrat information about character archetypes from the plot text. We implemet two methods: Latent Dirichlet Allocation (LDA)-based and BERT-based.

Latent Dirichlet Allocation-based clustering:
- extract linguistic features for each character (attributes, active and patient verbs),
- use word2vec embeddings to cluster this features into topics,
- perform Latent Dirichlet Allocation to cluster characters based of their features topics.
  
BERT-based clustering:
- obtain character's embedding as the mean of the pretrained BERT embeddings of character's name tokens in the text of the plot,
- performe clustering using this embeddings.

Then we compare the quality of our clustering methods with the quality of the clustering proposed in the paper "Learning Latent Personas of Film Characters". The performance of our LDA-based clustering is better when comparing Variation of Information between learned clusters and gold clusters extracted from TV Tropes ([refer](http://www.cs.cmu.edu/~dbamman/pubs/pdf/bamman+oconnor+smith.acl13.pdf) to the paper for the details).


3) Linear regression
4) Hypothesis testing

    In order to compare the success of the actors who play characters of different archetypes we use hypothesis testing in order to determine if there is statistical difference in the succes metric between groups of actors.

## Proposed timeline
17-11 
- Proof of concept (P2 deadline)

24-11 
- Choose the best clustering algorithm
- Finalize the success metric for the movies and the actors

01-12
- Perform analysis

08-12 
- Clean the code

15-12 
- Draft Data Story

22-12 
- Final Data Story (P3 deadline)

## Organization within the team: A list of internal milestones up until project Milestone P3.

## Questions for TAs (optional): Add here any questions you have for us related to the proposed project.


**REMINDER**: 

For submission:
Readme.md file containing the detailed project proposal (up to 1000 words)
Notebook containing initial analyses and data handling pipelines. We will grade the correctness, quality of code, and quality of textual descriptions.
