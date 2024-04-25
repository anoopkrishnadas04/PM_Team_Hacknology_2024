from flask import Flask, request, jsonify
from get_anime_list import get_anime_list
from getAnimeRecs import get_anime_recs_formatted

app = Flask(__name__)

#@app.route("/fget_anime_list/<string:username>", methods=["GET"])
#def fget_anime_list(username):
#    return get_anime_list(username_input=username), 200


@app.route("/fget_anime_recs/<string:username>/<string:fav_tv_show>", methods=["GET"])
def fget_anime_recs(username, fav_tv_show):
    return jsonify(get_anime_recs_formatted(username=username, fav_tv_show=fav_tv_show))

if __name__ == "__main__":
    app.run(debug=True)