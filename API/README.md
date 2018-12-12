To run this API you simple need to run
```
    python app.py
```
This will produce a url which will take you to the user interface.

## System Requirements:

## System features:
### navigation bar
At the top of the page is the navigation bar, it has the following items:
1. search for movie by name (search bar)
2. go to home page (clicking name 'Melon')
3. go to profile  (menu on the right)
4. log out (menu on the right)  

The search makes use of stopwords which uses nltk library (it will prompt for some files to be downloaded before you can continue running the API)

### welcome page
This is the first page you see when you go to the url. you can:
1. login 
2. register  

Before you can access the system and for the purpose of this assignment, you must either login or register in the system. This data is stored in the data file in users.csv.
upon inspection of the csv you would notice that there are already some registered users those users are 'fred0' to 'fred610' the passwords for them is the same as the name. 

### Register page
In this page you can set a username and password. you can also choose your preferred genres for movies. There are no high level validations on the inputs (choose a username that is not in the users.csv or else this might cause issues when it comes to creating the profile)


### movies list page
1. recommended movies based on ratings 
2. recommended movies based last viewed item
3. list of all movies  

If a search is fired, the recommendations will not appear; they always appear when you go to the home page or have an empty search. Two methods are used for recommendations the ratings matrix factorization based on user ratings and ratings correlation based on certain movie ratings. The general list of movies is used for the search functionality. The movie appear in cards with each card has some basic information about the movie such as title, genres and average rating. A button in the cards navigate to the movie page.

### movie details page
1. movie details
2. tags related to the movie
3. rating functionality 

This page has the movie details along with some tags about the movie. There is a rating button which will prompt a popup window that will allow you to rate the movie or if you have already rated for the movie to change the rating; all changes are reflected to the ratings.csv file. 

### user profile page
1. user details such as username and password
2. preferred genres 
3. list of rated movies
4. list of top ten searched words
5. list of top ten searched genres

This page contains all the basic information about the user (you). The username, password and preferred genres are static data and can be updated; the user has full control over this data. The lists however are dynamic data that are collected based on the user behaviour (using the search bar/ going to the movie page). The list of rated movies shows the user rating for each movie. 

## Included files
### recommendation engine
There is a python class that has all the recommendation mechanisms used and is the access point to the movies and ratings data (available in the data folder). The small dataset from movielens was used due to the performance of the recommendation algorithms - especially when it comes to creating the pivot tables that are used to get recommendations. It also pulls the data for the tags. 

main functions:
1. get movie based on movie id 
1. get movie tags based on movie id 
1. get all movie genres possible 
1. get all user ratings based on user id
4. get movies based on a search term
6. update ratings

For updating the ratings with the user's new rating, the ratings.csv is updated and all the other data that use the ratings such as the data for recommendations.

### templates
All html files used can be found in the templates/ directory. They are in jinja2 format; compatible with flask and allows creating for loop and passing data to the html page. 

### service
This script links the recommendation engine to the user inputs and interactions with the UI. It controls the creating and maintaining the user profile. All user related interactions can be found there.

main functions:
1. login check (used to retrieve userId)
2. get user static data (username, password, preferred genre)
3. set user profile (this is for initialization and updates)
4. create user profile (new profile)
5. search movies
6. get recommendations 
7. get last clicked movie
8. update user data

There are some other functions but those are the main ones and most used. When a user searches for a movie the terms that they used are stored in a list with a count for how many times the term has been searched. The top results from the search is used as the base for the search genre that is stored as part of the user profile; a count is also kept for this (data/ directory for all csvs)