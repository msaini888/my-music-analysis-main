# My Spotify Data Analysis: Overview

In this project I have gathered my listening history from my spotify account. Then performed data analysis on it to get a better understanding of my listening history, music taste, and choice of artist.

Moreover, performed a cluster analysis on the dataset.

## Codes and Resources used

- Editor used: VS code
- Python version: 3.9.4
- Packages used: pandas, matplotlib, seaborn, calplot, sklearn, spotipy, requests
- Data scraper 1: [Blog](https://towardsdatascience.com/get-your-spotify-streaming-history-with-python-d5a208bbcbd3) and [GitHub](https://github.com/vlad-ds/spoty-records)
- Data scraper 2: [Blog](https://towardsdatascience.com/viz-your-music-with-spotify-api-and-plotly-eaa65f652191) and [GitHub](https://github.com/VincyHu/MusicForYou)

## About the Dataset

The data is scraped from Spotify using it's API.

## Data Cleaning

The data is then preprocessed and transformed as required to avoid any abberations that might later skew the results. 

The data cleaning steps that are performed are:
- Dropping duplicate columns
- Dropping duplicate rows
- Null check
- Data Format check
- Value check

## Exploratory Data Analysis

A few of the visualizaton highlights are:
![streaming_history](https://github.com/Mohit020888/my-music-analysis-main/assets/63721227/5b3cf1be-29e4-4184-91af-61d882b50328)

![song_modes_distribution](https://github.com/Mohit020888/my-music-analysis-main/assets/63721227/6506fe88-eb75-4bfb-8bb2-7716d8ae2d3c)


## Cluster Analysis

Various cluster analysis are performed to group and define the cluster profiles of the songs.

Different cluster algorithms performed are:
- KMeans clustering
- Agglomerative clustering
- Affinity Propagation Clustering
- BIRCH
- DBSCAN
- Mini-Batch Kmeans
![clustering_kmeans](https://github.com/Mohit020888/my-music-analysis-main/assets/63721227/84cf37d5-2f95-4f58-a681-3d30bc754254)



## Blog Links

If you prefer an in-depth explanation for the code in this repository, you can go through the following articles:

- https://medium.com/analytics-vidhya/spotify-music-data-analysis-part-1-c8457bfc53a
- https://medium.com/analytics-vidhya/spotify-music-data-analysis-part-2-3a69ae0f7f01
- https://medium.com/analytics-vidhya/spotify-music-data-analysis-part-3-9097829df16e
- https://medium.com/analytics-vidhya/spotify-music-data-analysis-part-4-4016e2954795
