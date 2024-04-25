import pandas as pd
import type_isolation as t
import genre_likeness as gl
import get_anime_list as gal
import length_preference as lp
import keywordAnalysis as ka
import json

def get_anime_recs(username, fav_tv_show):
    #######################################
    #opening the updated csv that reflects our new scores
    anime_df = pd.read_csv('updated-anime-dataset-2023.csv')

    ####################################### CODE NEEDS TO BE WRITTEN
    #user chooses whether they would like to get movies, shows, or both
    #as of now it only works for shows
    user_input = 'TV'
    anime_df = t.update_df_by_type(anime_df, user_input)
    print("data frame updated to be specifically one type")

    #######################################
    #User MAL is inputted, as of now it will only be functional with a user MAL
    #username = "holesumname"#sample input
    #generating a list of all of the anime ids of watched anime
    id_arr = gal.get_anime_list(username)
    anime_df = anime_df = gl.compute_genre_likeness(anime_df, id_arr)
    print("genre likeness calculated")


    ########################################
    #generating the length difference scores
    anime_df = lp.apply_length_difference(anime_df, id_arr)

    ########################################
    #filter out anime the user has already watched
    anime_df = anime_df[~anime_df['anime_id'].isin(id_arr)]

    ######################################## CODE NEEDS TO BE WRITTEN
    #as of now the likeness score is calculated by the genre likeness, the length likeness, and soon to be the keyword analysis
    #keyword analysis returns a perentage of similairity whilst length likeness is an integer value between 0 and 4 with lower 
    #values being better, and genre likeness is returned as a percentage
    anime_df = anime_df.assign(final_likeness = lambda x: (x['newScore']*x['genre likeness']*x['lengthLikeness']))
    anime_df = anime_df.sort_values(by='final_likeness', ascending=False)
    filter_anime_df = anime_df.head(5000)

    ########################################
    #this is where keyword analysis takes place on the top 5000? anime based on similairity score
    filter_anime_df = ka.keyword_analysis(filter_anime_df, anime_df, fav_tv_show)

     ########################################
     #here we are applying a popularity score to make sure that recommendations return anime the user
     #would be interested in
    def apply_pop(pop):
        return 1 - (pop/50000)

    filter_anime_df['popScore'] = filter_anime_df['Popularity'].apply(apply_pop)

     ########################################
     #here we are calculating the official final score for similairity
    filter_anime_df = filter_anime_df.assign(final_likeness = lambda x: x['final_likeness']*x['popScore']*x['keywordScore'])
    filter_anime_df = filter_anime_df.drop(['Other name'], axis = 1)

    #print statement for testing purposes
    print(filter_anime_df.sort_values(by='final_likeness', ascending=False).head(10))

    ######################################## 
    #the data frame is returned to the user in order of score and similairity
    return(filter_anime_df.sort_values(by='final_likeness', ascending=False))


def get_anime_recs_formatted(username, fav_tv_show):
    temp_df = get_anime_recs(username, fav_tv_show)
    
    top_anime_recs = []
    for i in range(10):
        index = temp_df['Name'].index[i]
        top_anime_recs.append(
            {
                "anime_actual_rank":    int(i),
                "name":                 str(temp_df["Name"][index]),
                "english_name":         str(temp_df["English name"][index]),
                "anime_id":             int(temp_df["anime_id"][index]),
                "score":                float(temp_df["Score"][index]),
                "genres":               list(str(temp_df["Genres"][index]).split(", "))
            }
        )
    return top_anime_recs
#get_anime_recs_formatted("holesumname")