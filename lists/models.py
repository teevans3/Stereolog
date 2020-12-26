from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField


# Only storing albums when they're added to a list (to reduce api calls)
class Album(models.Model):
    name = models.CharField(max_length=900)
    album_id = models.CharField(max_length=62)
    artist = models.CharField(max_length=300)
    artist_id = models.CharField(max_length=62)
    cover_art_url = models.TextField()

    def __str__(self):
        return f"Name: {self.name}.....Artist: {self.artist}.....Album ID: {self.album_id}.....Artist ID: {self.artist_id}"


class List(models.Model):
    title = models.CharField(max_length=200, null=True)
    title_slug = models.SlugField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    author = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)
    albums = models.ManyToManyField(Album)

    def __str__(self):
        return f"Title: {self.title}.....User: {self.author}.....Date: {self.date}.....Description: {self.description}"

    def get_absolute_url(self):
        return reverse('list_detail', kwargs={'title_slug': self.slug})
