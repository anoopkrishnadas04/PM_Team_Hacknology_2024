import pandas as pd
import type_isolation as t
import genre_likeness as gl
import get_anime_list as gal
import length_preference as lp
import keywordAnalysis as ka
def get_anime_recs(username):
    anime_df = pd.read_csv('updated-anime-dataset-2023.csv')

    ####################################### CODE NEEDS TO BE WRITTEN
    #user chooses whether they would like to get movies, shows, or both
    user_input = 'TV'
    anime_df = t.update_df_by_type(anime_df, user_input)
    print("data frame updated to be specifically one type")

    ####################################### CODE NEEDS TO BE WRITTEN
    #User MAL is inputted, as of now it will only be functional with a user MAL
    #username = "holesumname"#sample input
    #generating a list of all of the anime ids of watched anime
    id_arr = gal.get_anime_list(username)
    anime_df = anime_df = gl.compute_genre_likeness(anime_df, id_arr)
    print("genre likeness calculated")


    ########################################
    anime_df = lp.apply_length_difference(anime_df, id_arr)

    ########################################    
    #key word analysis goes here

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

    filter_anime_df = ka.keyword_analysis(filter_anime_df, anime_df)

    def apply_pop(pop):
        return 1 - (pop/50000)

    filter_anime_df['popScore'] = filter_anime_df['Popularity'].apply(apply_pop)
    filter_anime_df = filter_anime_df.assign(final_likeness = lambda x: x['final_likeness']*x['popScore']*x['keywordScore'])
    filter_anime_df = filter_anime_df.drop(['Other name'], axis = 1)

    print(filter_anime_df.sort_values(by='final_likeness', ascending=False).head(10))
    ######################################## CODE NEEDS TO BE WRITTEN
    #the data frame is then returned to the user in order of score and similairity
    return(anime_df)
get_anime_recs("holesumname")
