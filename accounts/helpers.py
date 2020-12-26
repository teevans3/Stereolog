from lists.models import Album


# Function for adding an album to the list, checking for duplicates
def add_album(list_albums, album_id):

    already_stored = False

    # Retrieve all albums in the database
    all_albums = Album.objects.all()

    for i in range(len(all_albums)):
        if all_albums[i].album_id == album_id:
            already_stored = True

    # If already stored in the database, no need to create a new object for it
    if already_stored == True:
        # If there are albums in the list, make sure the album is not already in it
        if len(list_albums) > 0:
            for album in range(len(list_albums)):
                if list_albums[album].album_id == album_id:
                    return "duplicate album"

        return "album in database"

    else:
        return "new album to add"


# Function to check if user is viewing their own profile
def viewing_self(profile_username, session_user):

    if str(profile_username) == str(session_user):
        return True
    else:
        return False
