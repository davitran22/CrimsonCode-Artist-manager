from flask import Flask, render_template, request # flask headers
from spotify_api import get_token, search_for_artist, get_top_songs_by_artist, get_artist_profile_picture, get_artist_followers
#Import the spotify_api file and then import the functions to display artist information

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def index():

    if request.method == "POST":
        artist_name = request.form["artist_name"] # retrieve the artists from user
        token = get_token() # the token is the client information
        artist = search_for_artist(token, artist_name) # get the artists information based on the search

        if not artist:
            return render_template("index.html", error="Artist not found. Please try again.")

        artist_id = artist["id"] # retreive the artists id field which acts like the key to the other fields
        profile_picture = get_artist_profile_picture(token, artist_id) # retreive the artists profile picture
        artist_followers = get_artist_followers(token, artist_id) # retrieve # of followers
        top_songs = get_top_songs_by_artist(token, artist_id) # retrieve the songs which is a list

        # the render template() function is used to display our data html pages
        # the data will be rendered to result.html which is another page
        return render_template(
            "result.html",
            artist_name=artist_name,
            profile_picture=profile_picture,
            artist_followers=artist_followers,
            top_songs=top_songs
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
