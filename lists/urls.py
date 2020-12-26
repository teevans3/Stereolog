from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path("", views.list_general, name=""),
    path("check_list_title", views.check_list_title, name="check_list_title")
    #path("<str:list_id>", views.user_list, name="user_list"),
    #path("<str:spotify_id>", views.album_detail, name="album_detail"),
]
