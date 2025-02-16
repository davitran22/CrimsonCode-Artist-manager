from dotenv import load_dotenv
import os
import json
import base64
from requests import post, get
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#print(client_id, client_secret)


def get_token():
    # Get token from API
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "authorization": "Basic " + auth_base64,
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }
   
    result = requests.get(url, headers=headers, params=params)
    
    if result.status_code != 200:
        print(f"Error: {result.status_code}: {result.text}")
        return
    json_result = json.loads(result.content)["artists"]["items"]
    if len((json_result)) == 0:
        print("No artist found")
        return None
    return json_result[0]
    
    
    
def get_top_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?country=US"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    
    for idx, album in enumerate(json_result["items"], start=1):
        print(f"{idx + 1}. {album['name']} ({album['release_date']})") 
    return json_result
    
    




 
token = get_token()
result = search_for_artist(token, "lil uzi vert")
artist_id = result["id"]
songs = get_top_songs_by_artist(token, artist_id)

print(result)


"""for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
    print(f"Popularity: {song['popularity']}") """
    

#get_albums_by_artist(token, artist_id) #prints out the albums of the artist

