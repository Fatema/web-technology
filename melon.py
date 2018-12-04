#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # Load Data

# In[2]:


movies = pd.read_csv('ml-latest/movies.csv')


# In[3]:


ratings = pd.read_csv('ml-latest/ratings.csv')


# In[4]:


tags = pd.read_csv('ml-latest/tags.csv')


# In[5]:


links = pd.read_csv('ml-latest/links.csv')


# In[6]:


genome_tags = pd.read_csv('ml-latest/genome-tags.csv')


# In[7]:


genome_scores = pd.read_csv('ml-latest/genome-scores.csv')


# # Manipulate Data

# Extract the year from the movie title and store it in a seperate column (not all movies have the year so those will have a value of 0)

# In[8]:


movies['year'] = movies['title'].str.extract(r'\((\d{4})\)', expand=False).astype('float64').fillna(0).astype('int64')


# In[9]:


print(movies.dtypes)


# In[10]:


print(movies.shape)


# In[11]:


print(movies.head())


# retrieve all the genres available in the movies table

# In[12]:


genres = set(movies['genres'].str.cat(sep='|').split('|'))


# In[13]:


print(genres)


# In[14]:


print(ratings.dtypes)


# In[15]:


print(ratings.head())


# # Data Aggregation 

# In[16]:


movie_data = pd.merge(ratings, movies, on='movieId')


# In[17]:


print(movie_data.head())


# In[18]:


rating_mean = movie_data.groupby('movieId')['rating'].mean().sort_values(ascending=False).reset_index().rename(columns={'rating':'ratingAvg'})


# In[ ]:


print(rating_mean.head())


# In[ ]:


rating_count = movie_data.groupby('movieId')['rating'].count().sort_values(ascending=False).reset_index().rename(columns={'rating':'count'})


# In[ ]:


rating_count_mean = pd.merge(rating_count, rating_mean, on='movieId')


# In[ ]:


print(rating_count_mean.head())


# In[ ]:


movie_data.loc[movie_data['movieId'] == 1]


# # Movie Recommendation System

# This bit is all from https://stackabuse.com/creating-a-simple-recommender-system-in-python-using-pandas/

# In[ ]:


ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean()) 


# In[ ]:


print(ratings_mean_count.head())


# In[ ]:


ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())  


# In[ ]:


print(ratings_mean_count.head())


# Reset the index as the grouping mixes them up

# In[ ]:


ratings_mean_count = ratings_mean_count.reset_index()


# In[ ]:


print(ratings_mean_count.head())


# In[ ]:


import matplotlib.pyplot as plt  
import seaborn as sns  
sns.set_style('dark')  
get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(8,6))  
plt.rcParams['patch.force_edgecolor'] = True  
ratings_mean_count['rating_counts'].hist(bins=50)  


# In[ ]:


plt.figure(figsize=(8,6))  
plt.rcParams['patch.force_edgecolor'] = True  
ratings_mean_count['rating'].hist(bins=50) 


# In[ ]:


plt.figure(figsize=(8,6))  
plt.rcParams['patch.force_edgecolor'] = True  
sns.jointplot(x='rating', y='rating_counts', data=ratings_mean_count, alpha=0.4)  


# To create the matrix of movie titles and corresponding user ratings

# In[ ]:


user_movie_rating = movie_data.pivot_table(index='userId', columns='title', values='rating')  


# In[ ]:


user_movie_rating.head()  


# In[ ]:


forrest_gump_ratings = user_movie_rating['Forrest Gump (1994)']


# In[ ]:


forrest_gump_ratings.head() 


# In[ ]:


movies_like_forest_gump = user_movie_rating.corrwith(forrest_gump_ratings)

corr_forrest_gump = pd.DataFrame(movies_like_forest_gump, columns=['Correlation'])  
corr_forrest_gump.dropna(inplace=True)  
corr_forrest_gump.head()  


# In[ ]:


corr_forrest_gump.sort_values('Correlation', ascending=False).head(10) 


# In[ ]:


corr_forrest_gump = corr_forrest_gump.join(ratings_mean_count['rating_counts'])  
corr_forrest_gump.head() 


# In[ ]:




