import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from .models import List
from .helpers import create_new_list, convert_lists


def list_general(request):

    # Retrieve 6 most recently-created lists, then convert them for displaying on web page
    lists = List.objects.all().order_by('-date')[:6]
    recent_lists = convert_lists(lists)

    # If user is creating a new list
    if request.method == "POST":
        # Retrieve session user, all lists created by user, as well as new list title & description
        user = request.user
        user_lists = List.objects.filter(author__icontains=user)
        new_title = request.POST['list_title']
        new_description = request.POST['list_description']

        # Create the new list, assuming all requirements are met; then redirect user to new list page
        if create_new_list(user, user_lists, new_title, new_description) == "success":
            return redirect(f"/accounts/{user}/lists/{slugify(new_title)}")

        else:
            return HttpResponse("You already have a list with that name.")

    return render(request, "lists/list_general.html", {"recent_lists": recent_lists})


# Function for checking user already has a list with the same title upon list creation
def check_list_title(request):

    data = {'unique_title': True}

    if request.method == "GET":
        # Retrieve already-existing list titles and convert them to upper-case for comparison
        user_lists = List.objects.filter(author__icontains=request.user)
        list_titles = []

        for i in range(len(user_lists)):
            list_titles.append(user_lists[i].title.upper())

        # Retrieve new list title from the AJAX request, then compare it to all user's list titles
        new_list_title = request.GET.get('new_list_title').upper()

        for i in range(len(list_titles)):
            if list_titles[i].replace(" ", "") == new_list_title.replace(" ", ""):
                data['unique_title'] = False

    return JsonResponse(data)
