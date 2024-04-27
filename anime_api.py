from flask import Flask, request, jsonify, Response
from get_anime_list import get_anime_list
from getAnimeRecs import get_anime_recs_formatted

app = Flask(__name__)

#@app.route("/fget_anime_list/<string:username>", methods=["GET"])
#def fget_anime_list(username):
#    return get_anime_list(username_input=username), 200


@app.route("/fget_anime_recs/<string:username>")
def fget_anime_recs(username):
    # username = request.args.get("username")
    fav_tv_show = request.args.get("fav_tv_show")
    print(fav_tv_show)

    anime_recs_response = {
        "data": get_anime_recs_formatted(username=username, fav_tv_show=fav_tv_show),
        "response_id": 200
    }

    return jsonify(anime_recs_response), {"Access-Control-Allow-Origin": "*"}


if __name__ == "__main__":
    app.run(debug=True)