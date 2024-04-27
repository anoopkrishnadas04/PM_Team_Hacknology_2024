# AniLyst
  This is an anime recommender program that allows users to input their MyAnimeList username and their favorite anime (for the sake of keyword analysis) and it returns to them a list of the anime most similar to their past watch history and favorite anime.   
    
  When tasked to create a data science project for Hacknology 2024 we decided to attempt to tackle a problem all three of us had dealt with constantly. That is not ever knowing what to watch and being tired of receiving the same flat-recommended anime from friends. In order to set out and solve this problem we first found a recent dataset containing a comprehensive list of anime from Kaggle. We then decided to use Pandas to handle the dataset as we were all comfortable with writing in Python and had partial experience with Pandas. We then decided we would base our recommendation score based off of genre, length, and keyword analysis. We also decided to refit the scores of our dataset to only reflect scores given by users who had watched over 25 anime as we felt their taste had not developed enough to give accurate scores. We also removed all user scores of users who had a median score of 8.5 or higher as well as 2.5 or lower to remove bots who were used only to harm or help anime scores. We decided to also implement the MyAnimeList API to recieve the users past watch list. We then run our genre, length, and keyword analysis against the shows in the dataset with our users past watch history and the anime they are looking for recommendations based off of. We then took that value and multiplied it to the dataset's updated scores and factored in popularity of shows as well. Following the processes the user is shown the top ten shows that are most similair to the users input.     
    
  In terms of problems, there was many. We had all seen pandas and used it on and off, but this project required an in-depth use of it. We also faced heavy difficulties writing the keyword analysis machine learning. This was a task that took us hours of discord calls to resolve. We also had trouble dealing with incorrect or partial inputs. For the user's MyAnimeList username there isn't much we can do other than ask them to try again, but for the anime input we realised a simple string comparison wouldn't work. For some reason that did not allow partial inputs for anime that had special characters in the title. To deal with this we converted the dataframe titles and the user's input to regex, and that solved our problem. We also decided we wanted the program to be easily used, to do this we had to create a flask api and a website for our program, this was something we couldn't have completed without the deadline extensions, though we didn't consider the idea until the deadline was originally extended.      
    
  We would really like to continue working on this program following the end of the hackathon and already have some ideas. We are planning on adding a feature to do the same thing we do for anime, for manga instead. This would be a relatively simple process, but it will also be very time consuming. We would also like to get it working for movies using the letterbox api. Finally we would like to create our own dataset by webscraping MyAnimeList to have an even more recent dataset.

Dataset:  
https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset  

Youtube Demo:
https://youtu.be/vspmhPgoyoo
        
Contributors:  
anoopkrishnadas04: Anoop K.  
holesum: Dylan S.  
Alex-Pat-1: Alex P.

This code requires the following packages:
1. Pandas  
2. NumPy  
3. Gensim
4. NTLK
5. pickle
