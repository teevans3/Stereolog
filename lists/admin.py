from django.contrib import admin
from django.forms import TextInput, Textarea
from .models import List, Album

admin.site.register(List)
admin.site.register(Album)
