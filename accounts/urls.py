from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<str:username>/", views.profile, name="profile"),
    path("<str:username>/likes", views.liked_albums, name="liked_albums"),
    path("<str:username>/reviews", views.reviews, name="reviews"),
    # Use an album_id instead of a slug because some albums have the same name (unfortunately the URL won't be as pretty as a slug)
    path("<str:username>/reviews/<str:album_id>", views.review_detail, name="review_detail"),
    path("<str:username>/lists", views.lists, name="lists"),
    path("<str:username>/lists/<slug:title_slug>", views.list_detail, name="list_detail"),
    path("check_user_info", views.check_user_info, name="check_user_info"),
    path("check_album_in_list", views.check_album_in_list, name="check_album_in_list")

]
