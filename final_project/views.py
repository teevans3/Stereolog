import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from albums.models import Review
from lists.models import List
from lists.helpers import convert_lists


def index(request):

    # Retrieve 10 popular albums, 3 popular reviews, and 4 popular lists (convert lists for display)
    popular_albums = Review.objects.filter(like__icontains="YES").order_by('-date')[:10]
    popular_reviews = Review.objects.all().order_by('?')[:3]
    longest_lists = List.objects.annotate(q_count=Count('albums')).order_by('-q_count')[:4]
    popular_lists = convert_lists(longest_lists)

    context = {
        "popular_albums": popular_albums,
        "popular_reviews": popular_reviews,
        "popular_lists": popular_lists
    }

    return render(request, "index.html", context)
