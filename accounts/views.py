import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from django.contrib.auth import login, logout
from django.apps import apps
from django.db.models import Q
from albums.models import Review
from lists.models import List
from lists.models import Album
from .helpers import add_album, viewing_self
from lists.helpers import convert_lists, create_new_list
from final_project.helpers import request_spotify_data


def register(request):

    # If user is already logged in, redirect them to the homepage
    if request.user.is_authenticated:
        return redirect("/")

    # If user is creating an account, ensure form is valid and requirements are fulfilled
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            # Save the register form (which will return the newly-created user) and log them in
            user = register_form.save()
            login(request, user)
            return redirect("/")
        else:
            return render(request, "accounts/register.html", {"register_form": register_form})

    return render(request, "accounts/register.html", {"register_form": UserCreationForm()})


def login_view(request):

    # If user is already logged in, redirect them to the homepage
    if request.user.is_authenticated:
        return redirect("/")

    # If user is logging in, ensure form is valid and requirements are fulfilled
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            # Retrieve user from form to log them in
            user = login_form.get_user()
            login(request, user)
            return redirect("/")
        else:
            # FIND A WAY TO JUST DISPLAY ERRORS RATHER THAN SEND A MESSAGE (like we do with register form)
            message = "Invalid username or password."
            return render(request, "accounts/login.html", {"login_form": login_form, "message": message})

    return render(request, "accounts/login.html", {"login_form": AuthenticationForm()})


def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("/")


def profile(request, username):
    # Retrieve profile the user is visiting and the session user; check if user is viewing their own profile
    profile_username = username
    session_user = request.user
    my_profile = viewing_self(profile_username, session_user)

    # Retrieve most recent 3 reviews, most recent 2 lists (convert for display), and most recent 5 liked albums
    recent_reviews = Review.objects.filter(author__icontains=profile_username).order_by('-date')[:3]
    lists = List.objects.filter(author__icontains=profile_username).order_by('-date')[:2]
    recent_lists = convert_lists(lists)
    recently_liked_albums = Review.objects.filter(Q(like__icontains="YES") & Q(author__icontains=profile_username)).order_by('-date')[:5]

    context = {
        "my_profile": my_profile,
        "profile_username": profile_username,
        "recent_reviews": recent_reviews,
        "recent_lists": recent_lists,
        "recently_liked_albums": recently_liked_albums
    }

    return render(request, "accounts/profile.html", context)


def reviews(request, username):
    # Retrieve profile the user is visiting and the session user; check if user is viewing their own profile
    profile_username = username
    session_user = request.user
    my_profile = viewing_self(profile_username, session_user)

    # Retrieve all reviews
    reviews = Review.objects.filter(author__icontains=profile_username).order_by('-date')

    context = {
        "my_profile": my_profile,
        "profile_username": profile_username,
        "reviews": reviews
    }

    if not reviews:
        return HttpResponse("This user has not written any reviews yet.")

    else:
        return render(request, "accounts/reviews.html", context)


# Each user's unique LISTS page (all created lists by user)
def lists(request, username):
    # Retrieve profile the user is visiting and the session user; check if user is viewing their own profile
    profile_username = username
    session_user = request.user
    my_profile = viewing_self(profile_username, session_user)

    # Retrieve all lists (and convert for display)
    lists = List.objects.filter(author__icontains=profile_username).order_by('-date')
    all_lists = convert_lists(lists)

    context = {
        "my_profile": my_profile,
        "profile_username": profile_username,
        "lists": all_lists
    }

    if not lists:
        return HttpResponse("This user has not created any lists yet.")

    else:
        return render(request, "accounts/lists.html", context)


def liked_albums(request, username):
    # Retrieve profile the user is visiting and the session user; check if user is viewing their own profile
    profile_username = username
    session_user = request.user
    my_profile = viewing_self(profile_username, session_user)

    # Retrieve all liked albums
    liked_albums = Review.objects.filter(Q(author__icontains=profile_username) & Q(like__icontains="YES")).order_by('-date')

    context = {
        "my_profile": my_profile,
        "profile_username": profile_username,
        "liked_albums": liked_albums
    }

    if not liked_albums:
        return HttpResponse("This user has not liked any albums yet.")

    else:
        return render(request, "accounts/liked_albums.html", context)


def review_detail(request, username, album_id):
    # Retrieve profile the user is visiting and the session user; check if user is viewing their own profile
    profile_username = username
    session_user = request.user
    my_profile = viewing_self(profile_username, session_user)

    # Retrieve the full review (if it exists)
    try:
        full_review = Review.objects.filter(Q(author__icontains=profile_username) & Q(album_id__icontains=album_id))[0]
    except IndexError:
        return HttpResponse("This user has not written a review for this album.")

    context = {
        "my_profile": my_profile,
        "profile_username": profile_username,
        "full_review": full_review
    }

    if request.method == "POST":

        # Retrieve the review id
        review_id = request.POST['review_id']

        # If user is deleting the review
        if request.POST['review_form'] == "delete_review":

            # Delete the review
            Review.objects.filter(id=review_id).delete()

            # If the user has no reviews left, return them to their accounts page
            if not Review.objects.filter(author__icontains=profile_username):
                return redirect(f"/accounts/{session_user}")

            return redirect(f"/accounts/{session_user}/reviews")

        # If user is editing the review
        else:

            # Retrieve the review object that the user wants to edit
            edited_review = Review.objects.filter(id=review_id)

            # Update the review
            edited_review.update(rating=request.POST['rating'])
            edited_review.update(like=request.POST['like'])
            edited_review.update(text=request.POST['review'])

            # Update the review page
            context["full_review"] = Review.objects.filter(Q(author__icontains=profile_username) & Q(album_id__icontains=album_id))[0]

            return render(request, "accounts/review_detail.html", context)

    return render(request, "accounts/review_detail.html", context)


def list_detail(request, username, title_slug):
    # Retrieve profile the user is visiting and the session user; check if user is viewing their own profile
    profile_username = username
    session_user = request.user
    my_profile = viewing_self(profile_username, session_user)

    # Retrieve the full list and the albums in the list
    try:
        list_info = List.objects.filter(Q(author__icontains=profile_username) & Q(title_slug__icontains=title_slug))[0]

    except IndexError:
        return HttpResponse("This list does not exist.")

    list_albums = list_info.albums.all()

    context = {
        "my_profile": my_profile,
        "list_info": list_info,
        "list_albums": list_albums
    }

    if request.method == "POST":

        # If user is searching for an album
        if request.POST['list_form'] == "album_search":
            # Retrieve the input from user and results to be displayed
            input = request.POST['album_name']
            results = request_spotify_data(input, "album_search")

            context.update({
                "search": input,
                "results": results
            })

            return render(request, "accounts/list_detail.html", context)

        # If user is adding an album to list
        elif request.POST['list_form'] == "add_album":

            # Retrieve the album_id of the album the user wishes to add
            album_id = request.POST['album_id']

            # Check if the album is already in the list..
            if add_album(list_albums, album_id) == "duplicate album":
                return HttpResponse("This album is already in your list.")

            else:
                # Check if the album is already in the Album database
                if add_album(list_albums, album_id) == "album in database":
                    new_album = Album.objects.filter(album_id__icontains=album_id)[0]

                else:
                    # Create a new Album object and save it to the database
                    new_album = Album()
                    new_album.name = request.POST['album_name']
                    new_album.album_id = album_id
                    new_album.artist = request.POST['artist_name']
                    new_album.artist_id = request.POST['artist_id']
                    new_album.cover_art_url = request.POST['cover_art_url']
                    new_album.save()

                # Update the user's list to include the album and retrieve the updated albums in the list
                list_info.albums.add(new_album)

        # If user is removing an album from list
        elif request.POST['list_form'] == "remove_album":

            # Remove that album from the list (still exists in the Album database, however)
            list_info.albums.remove(Album.objects.get(album_id__icontains=request.POST['album_id']))

        # If user is deleting list
        else:

            # Delete selected list
            List.objects.filter(id=request.POST['list_id']).delete()

            # If the user has no lists left, return them to their accounts page
            if not List.objects.filter(author__icontains=profile_username):
                return redirect(f"/accounts/{session_user}")
            else:
                return redirect(f"/accounts/{session_user}/lists")

        # Update the albums in the list
        context["list_albums"] = list_info.albums.all()

        return render(request, "accounts/list_detail.html", context)

    return render(request, "accounts/list_detail.html", context)


# Function for checking that the album does not already exist in the user's list
def check_album_in_list(request):

    data = {"duplicate": False}

    if request.method == "GET":

        # Retrieve the album (by id) the user wants to add and all the albums currently in the list
        album_id = request.GET.get('album_id')
        user_list_albums = List.objects.filter(Q(author__icontains=request.user) & Q(title__icontains=request.GET.get('list_title')))[0].albums.all()

        for i in range(len(user_list_albums)):
            if user_list_albums[i].album_id == album_id:
                data["duplicate"] = True

    return JsonResponse(data)


# Function for checking that user does have reviews, lists, likes upon clicking subnav links
def check_user_info(request):

    data = {
        "has_reviews": True,
        "has_lists": True,
        "has_likes": True
    }

    if request.method == "GET":

        # Retrieve the link clicked (for user reviews, lists, or likes)
        info_type = request.GET.get('info_type')

        # Check if user has any reviews
        if info_type == "reviews":
            if not Review.objects.filter(author__icontains=request.user):
                data["has_reviews"] = False

        # Check if user has any lists
        elif info_type == "lists":
            if not List.objects.filter(author__icontains=request.user):
                data["has_lists"] = False

        # Check if user has any likes
        else:
            if not Review.objects.filter(Q(author__icontains=request.user) & Q(like__icontains="YES")):
                data["has_likes"] = False


    return JsonResponse(data)
