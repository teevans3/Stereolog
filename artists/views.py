import requests
from django.shortcuts import render
from final_project.helpers import request_spotify_data


def artist_detail(request, artist_id):

    # Retrieve all artist information (returns as a dictionary)
    context = request_spotify_data(artist_id, "artist_display")

    return render(request, "artists/artist_detail.html", context)
