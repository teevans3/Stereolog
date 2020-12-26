import os
import requests
import base64
from operator import itemgetter


client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

# Function to perform authorization and return spotify access token to make web api calls
def authorize_spotify_api(client_id, client_secret):

    # Arguments for post request (from spotify api authorization guide)
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {"grant_type": "client_credentials"}

    client_code = f"{client_id}:{client_secret}"
    encoded_auth_code = base64.b64encode(client_code.encode())
    token_headers = {"authorization": f"Basic {encoded_auth_code.decode()}"}

    # request authorization via post request
    response = requests.post(token_url, data=token_data, headers=token_headers)

    if response.status_code not in range(200, 299):
        return False

    token_response = response.json()

    # Retrieve access token from json response
    return token_response["access_token"]


# Function for making api calls to retrieve spotify data (retrieving: new releases, input search, specific album info, or specific artist info)
def request_spotify_data(input, type):

    # Retrieve access token to create headers for api request
    access_token = authorize_spotify_api(client_id, client_secret)
    headers = {"Authorization": f"Bearer {access_token}"}

    # If request type is for displaying new releases
    if input == None and type == "new_releases":
        # Retrieve json data
        r = requests.get("https://api.spotify.com/v1/browse/new-releases?limit=50", headers=headers)
        results = r.json()

        # Convert results to a new list, keeping only relevant data
        results_albums = results['albums']['items']
        new_releases = []

        for i in range(len(results_albums)):
            album_info = {
                "name": results_albums[i]['name'],
                "artist": results_albums[i]['artists'][0]['name'],
                "cover_art_url":  results_albums[i]['images'][0]['url'],
                "album_id": results_albums[i]['id'],
                "artist_id": results_albums[i]['artists'][0]['id'],
            }

            new_releases.append(album_info)

        return new_releases

    else:
        # If request type is for an album search
        if type == "album_search":
            # Retrieve json data
            r = requests.get(f"https://api.spotify.com/v1/search?q={input}&type=album&limit=50", headers=headers)
            results_list = r.json()

            # Convert results from simplified album object to full album object (if there are matching results)
            simp_albums_info = results_list['albums']['items']

            if len(simp_albums_info) < 1:
                return "None"

            albums_info = []
            for i in range(len(simp_albums_info)):
                # Retrieve new json data of full album object
                lookup_album_url = simp_albums_info[i]['href']
                r = requests.get(lookup_album_url, headers=headers)
                full_info = r.json()

                albums_info.append(full_info)

            # Reorder albums based on popularity
            try:
                sorted_albums_info = sorted(albums_info, key=itemgetter('popularity'), reverse=True)
            except KeyError:
                sorted_albums_info = albums_info

            # Convert results to a new list, keeping only relevant data
            results = []
            for i in range(len(sorted_albums_info)):
                item_info = {
                    "album": sorted_albums_info[i]['name'],
                    "artist": sorted_albums_info[i]['artists'][0]['name'],
                    "artist_id": sorted_albums_info[i]['artists'][0]['id'],
                    "album_id": sorted_albums_info[i]['id'],
                }

                # Check if there are images associated with album cover
                if len(sorted_albums_info[i]['images']) < 1:
                    item_info.update({"cover_art_url": None})
                else:
                    item_info.update({"cover_art_url": sorted_albums_info[i]['images'][0]['url']})

                results.append(item_info)

            return results

        # If request type is for an album display
        elif type == "album_display":
            # Retrieve json data
            r = requests.get(f"https://api.spotify.com/v1/albums/{input}", headers=headers)
            result = r.json()

            # Retrieve full artist object (so we can get first 5 genres, which is empty for album object)
            lookup_artist_url = result['artists'][0]['href']
            r = requests.get(lookup_artist_url, headers=headers)
            artist_result = r.json()

            # Retrieve only the first five genres listed (sometimes artists have 10+ genres)
            artist_genres = artist_result['genres']
            genres = []
            for i in range(len(artist_genres)):
                if i == 5:
                    break
                genres.append(artist_genres[i])

            # Retrieve list of track names
            album_tracks = result['tracks']['items']
            tracks = []
            for track in range(len(album_tracks)):
                tracks.append(album_tracks[track]['name'])

            # Convert all relevant data (including genres and tracks) to a dictionary
            album_info = {
                "album_id": input,
                "album_type": result['album_type'].capitalize(),
                # Does this accommodate for multiple artists?
                "artist": result['artists'][0]['name'],
                "artist_id": result['artists'][0]['id'],
                # Note: these are ARTIST (not album) genres; album genres are always empty for this API (bug?)
                "genres": genres,
                # Do we want all images or just one?
                "cover_art_url": result['images'][0]['url'],
                "name": result['name'],
                "popularity": result['popularity'],
                "release_date": result['release_date'],
                "tracks": tracks
            }

            return album_info

        # Or if request type is for an artist display
        else:
            # Retrieve json data
            r = requests.get(f"https://api.spotify.com/v1/artists/{input}", headers=headers)
            result = r.json()

            # Convert relevant artist data to a dictionary
            artist_info = {
                "name": result['name'],
                # Format the followers to have thousands separator
                "followers": f"{result['followers']['total']:,}",
                "genres": result['genres'][:5],
                "popularity": result['popularity']
            }

            # Check if there are images associated with artist
            if len(result['images']) < 1:
                artist_info.update({"artist_image_url": None})
            else:
                artist_info.update({"artist_image_url": result['images'][0]['url']})

            # Retrieve list of related artists
            k = requests.get(f"https://api.spotify.com/v1/artists/{input}/related-artists", headers=headers)
            result = k.json()
            artists = result['artists']

            # Convert related artists to a list of dictionaries (max 10) containing only relevant data
            related_artists = []
            for i in range(len(artists)):
                if i == 10:
                    break
                related_artist_info = {
                    "name": artists[i]['name'],
                    "artist_image_url": artists[i]['images'][0]['url'],
                    "related_artist_id": artists[i]['id']
                }
                related_artists.append(related_artist_info)


            # Retrieve all albums by artist
            lookup_url = f"https://api.spotify.com/v1/artists/{input}/albums/?limit=50"
            r = requests.get(lookup_url, headers=headers)
            result = r.json()

            albums = result['items']

            # Convert results to list of album dictionaries containing only relevant data
            artist_albums_info = []
            for i in range(len(albums)):
                # Make sure the album is by them (rather than being featured on it)
                if albums[i]['artists'][0]['name'] == artist_info['name']:
                    # Make sure album is not already in the list; if it is, skip it
                    multiple_album = False
                    for j in range(len(artist_albums_info)):
                        if artist_albums_info[j]['name'].upper() == albums[i]['name'].upper():
                            multiple_album = True

                    if multiple_album == False:
                        album_info = {
                            "name": albums[i]['name'],
                            "release_date": albums[i]['release_date'],
                            "album_id": albums[i]['id']
                        }
                        
                        # Check for album cover art
                        if len(albums[i]['images']) < 1:
                            album_info.update({"cover_art_url": None})
                        else:
                            album_info.update({"cover_art_url": albums[i]['images'][0]['url']})

                        artist_albums_info.append(album_info)

            artist_details = {
                "artist_info": artist_info,
                "related_artists": related_artists,
                "artist_albums_info": sorted(artist_albums_info, key = lambda i: i['release_date'], reverse=True)
            }

            return artist_details
