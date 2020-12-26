For my final project I created a web app, called StereoLog, that allows users to review albums and create lists of different albums. This application can be thought of as a more basic version of Letterboxd - in which I wanted a website where users could discuss albums, instead of movies. The data on albums and artists is retrieved from Spotify using api requests.



Some notes to mention:

  1) For Spotify's api, you cannot perform a general search by popularity; you must have some sort of search query. Thus, I had to get creative with the homepage's "popularity" of reviews, lists, and likes by basing it off of different factors.

  2) Upon searching for albums with type="album" in the api request, Spotify will return anything matching the description (even if it isn't specifically an album; could be a single). As such, even though this website is designed specifically for albums, I am allowing singles to exist as well.

  3) The create_new_list function (in lists/helpers.py) does not check if the title can be successfully be slugified (this presents problems when users create lists with special characters in the title, such as '@').

  4) When hovering over album images, the album-info will be displayed ("album name by album artist") and will stay displayed while the hover is on the album-info (to allow users to click the artist page link). This, however, is not applied to the list_detail page, as the album-info display constantly gets in the way of the add/remove-album buttons placed below the album image.



Below is a list of all the files contained in each app.

Root directory:

  base_layout.html - what all html files inherit from, includes the navbar

  index.html - homepage (displays "popular" albums, reviews, and lists)


Accounts app:

  profile.html - user's profile info (username, recent reviews, recent lists, recently-liked albums)

  login.html - web page for user to log in (needed for certain features)

  register.html - web page for user to create an account (needed for certain features)

  reviews.html - displays all user's reviews

  lists.html - displays all user's lists (features: ability create a new list)

  liked_albums.html - displays all user's liked albums

  review_detail.html - web page for user's full review (features: ability to edit or delete review)

  list_detail.html - web page for user's specific list (features: ability to search for an album, add/remove an album, and delete the list)

  helpers.py - functions for checking if an album exists in a user's list and determining whether the user logged in is viewing their own profile

  forms.py - edited UserCreationForm to include an email field and add validation errors


Albums app:

  album_general.html - general album page for displaying new releases and new reviews (features: ability to search for an album)

  album_detail.html - web page for specific album (features: ability to write a review)

  helpers.py - function for calculating the average rating of an album

  models.py - models for the Review objects


Artists app:

  artist_detail.html - web page for specific artist (and a list of their albums)


Final_project app (main):

  helpers.py - functions for performing spotify api authorization and for requesting spotify data via the api


Lists app:

  list_general.html - general lists page, displays recently-created lists (features: ability to create a new list)

  helpers.py - functions for creating a new list and converting lists for display

  models.py - models for the Album objects (only stored when an album is added to a list) and the List objects
