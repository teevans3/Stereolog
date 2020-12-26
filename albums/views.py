import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Review
from .helpers import avg_rating
from final_project.helpers import request_spotify_data


def album_general(request):

    # Retrieve new releases and most recent (10) reviews to be displayed
    context =  {
        "new_releases": request_spotify_data(None, "new_releases"),
        "reviews": Review.objects.all().order_by('-date')[:10]
    }

    # If user is searching for an album (or whatever search input)
    if request.method == "POST":
        # Retrieve user search input and results to be displayed
        input = request.POST['album_name']

        context.update({
            "results": request_spotify_data(input, "album_search"),
            "search": input
        })

        return render(request, "albums/album_general.html", context)

    return render(request, "albums/album_general.html", context)


def album_detail(request, album_id):

    # Retrieve: relevant info for album; (if there are any) likes, dislikes, & (average) ratings; and all reviews
    album_info = request_spotify_data(album_id, "album_display")

    try:
        album_rating = {
            "likes": len(Review.objects.filter(Q(album_id__icontains=album_id) & Q(like__icontains='YES'))),
            "dislikes": len(Review.objects.filter(Q(album_id__icontains=album_id) & Q(like__icontains='NO'))),
            "average_rating": avg_rating(Review.objects.filter(album_id__icontains=album_id))
        }

        reviews = Review.objects.filter(Q(album__icontains=album_info['name']) & Q(artist__icontains=album_info['artist'])).order_by('-date')

    except ZeroDivisionError:
        album_rating = None
        reviews = None

    context = {
        "album_info": album_info,
        "album_rating": album_rating,
        "reviews": reviews
    }

    # If user is submitting a review
    if request.method == "POST":
        # Retrieve user and make sure they do not already have a review for this album
        user = request.user
        existing_review = Review.objects.filter(Q(author__icontains=user) & Q(album_id__icontains=album_id))

        if not existing_review:
            # Create a new review object and add info from the review form
            review = Review()
            review.author = user
            review.album = request.POST['album']
            review.artist = request.POST['artist']
            review.text = request.POST['review']
            review.rating = request.POST['rating']
            review.like = request.POST['like']
            review.album_id = album_id
            review.artist_id = request.POST['artist_id']
            review.cover_art_url = request.POST['cover_art_url']
            review.save()

        else:
            return HttpResponse("You cannot submit more than one review!")

        # Update album_ratings and reviews
        context["album_rating"] = {
            "likes": len(Review.objects.filter(Q(album_id__icontains=album_id) & Q(like__icontains='YES'))),
            "dislikes": len(Review.objects.filter(Q(album_id__icontains=album_id) & Q(like__icontains='NO'))),
            "average_rating": avg_rating(Review.objects.filter(album_id__icontains=album_id))
        }
        context["reviews"] = Review.objects.filter(Q(album__icontains=album_info['name']) & Q(artist__icontains=album_info['artist'])).order_by('-date')

        return render(request, "albums/album_detail.html", context)

    return render(request, "albums/album_detail.html", context)
