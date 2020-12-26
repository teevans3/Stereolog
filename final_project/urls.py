from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("albums/", include('albums.urls')),
    path("accounts/", include('accounts.urls')),
    path("lists/", include('lists.urls')),
    path("artists/", include('artists.urls')),
    path("", views.index, name="index"),
]
