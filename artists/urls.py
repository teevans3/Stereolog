from django.urls import path
from . import views

urlpatterns = [
    path("<str:artist_id>", views.artist_detail, name="artist_detail"),
]
