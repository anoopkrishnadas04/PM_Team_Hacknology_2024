import pandas as pd
import type_isolation as t
import genre_likeness as gl
import get_anime_list as gal
import length_preference as lp

anime_df = pd.read_csv('updated-anime-dataset-2023.csv')

####################################### CODE NEEDS TO BE WRITTEN
#user chooses whether they would like to get movies, shows, or both
user_input = 'TV'
anime_df = t.update_df_by_type(anime_df, user_input)
print("data frame updated to be specifically one type")

####################################### CODE NEEDS TO BE WRITTEN
#User MAL is inputted, as of now it will only be functional with a user MAL
username = "holesumname"#sample input
#generating a list of all of the anime ids of watched anime
id_arr = gal.get_anime_list(username)
anime_df = anime_df = gl.compute_genre_likeness(anime_df, id_arr)
print("genre likeness calculated")
########################################    
#key word analysis goes here

########################################
anime_df = lp.apply_length_difference(anime_df, id_arr)


######################################## CODE NEEDS TO BE WRITTEN
#as of now the likeness score is calculated by the genre likeness, the length likeness, and soon to be the keyword analysis
#keyword analysis returns a perentage of similairity whilst length likeness is an integer value between 0 and 4 with lower 
#values being better, and genre likeness is returned as a percentage
anime_df = anime_df.assign(final_likeness = lambda x: (x['newScore']*x['genre likeness']*x['lengthLikeness']))
print(anime_df.sort_values(by='newScore', ascending=False).head())
######################################## CODE NEEDS TO BE WRITTEN
#the data frame is then returned to the user in order of score and similairity

