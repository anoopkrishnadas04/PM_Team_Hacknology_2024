# AniLyst
  This is an anime recommender program that allows users to input their MyAnimeList username and their favorite anime (for the sake of keyword analysis) and it returns to them a list of the anime most similar to their past watch history and favorite anime.   
    
  When tasked to create a data science project for Hacknology 2024 we decided to attempt to tackle a problem all three of us had dealt with constantly. That is not ever knowing what to watch and being tired of receiving the same flat-recommended anime from friends. In order to set out and solve this problem we first found a recent dataset containing a comprehensive list of anime from Kaggle. We then decided to use Pandas to handle the dataset as we were all comfortable with writing in Python and had partial experience with Pandas. We then decided we would base our recommendation score based off of genre, length, and keyword analysis. We also decided to refit the scores of our dataset to only reflect scores given by users who had watched over 25 anime as we felt their views had not developed enough to give accurate scores. We also removed all user scores of users who had a median score of 8.5 or higher as well as 2.5 or lower to remove bots who were used only to harm or help anime scores, or users whose ratings would only skew data.

Dataset:  
https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset  
        
Contributors:  
anoopkrishnadas04: Anoop K.  
holesum: Dylan S.  
Alex-Pat-1: Alex P.

This code requires the following packages:
1. Pandas  
2. NumPy  
3. Gensim
