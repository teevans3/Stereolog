from .models import List
from django.template.defaultfilters import slugify


# Function for user to create a new list
def create_new_list(user, user_lists, title, description):

    if len(user_lists) > 0:
        # Make sure the title is unique (no repeats allowed because of urls)
        for i in range(len(user_lists)):
            # Convert to all capital and accommodate for extra white space
            original_list_title = (user_lists[i].title).upper()
            new_list_title = title.upper()
            if original_list_title.replace(" ", "") == new_list_title.replace(" ", ""):
                return "failure"

    # Create a new list in List model (albums will be empty upon creation)
    list = List()
    list.title = title
    list.title_slug = slugify(title)
    list.description = description
    list.author = user
    list.save()

    return "success"


# Function for converting lists to include the list of cover_art_urls for first 5 albums
def convert_lists(lists):

    # New list to store the converted lists for display
    converted_lists = []

    # Ensure that there are indeed lists that exist
    if len(lists) < 1:
        return None

    # Retrieve first 5 albums in list and their respective cover_art_urls
    for i in range(len(lists)):

        cover_art_urls = []
        list_albums = lists[i].albums.all()[:5]

        for j in range(len(list_albums)):
            cover_art_urls.append(list_albums[j].cover_art_url)

        # If there are less than 5 albums in list , create "blank"/"empty" cover_art_urls (for display purposes)
        if len(cover_art_urls) < 5:
            empty_urls = 5 - len(cover_art_urls)
            cover_art_urls.extend([None] * empty_urls)

        # Recreate the new list info with added list of cover_art_urls
        list_info = {
            "title": lists[i].title,
            "title_slug": lists[i].title_slug,
            "author": lists[i].author,
            "date": lists[i].date,
            "cover_art_urls": cover_art_urls,
        }

        converted_lists.append(list_info)

    return converted_lists
