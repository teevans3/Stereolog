from django.urls import path
from . import views

urlpatterns = [
    path("", views.album_general, name=""),
    path("<str:album_id>", views.album_detail, name="album_detail"),
]
