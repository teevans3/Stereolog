from django.db import models


class Review(models.Model):
    rating_choices = (
        ('0.5 / 5.0', '0.5 / 5.0'),
        ('1.0 / 5.0', '1.0 / 5.0'),
        ('1.5 / 5.0', '1.5 / 5.0'),
        ('2.0 / 5.0', '2.0 / 5.0'),
        ('2.5 / 5.0', '2.5 / 5.0'),
        ('3.0 / 5.0', '3.0 / 5.0'),
        ('3.5 / 5.0', '3.5 / 5.0'),
        ('4.0 / 5.0', '4.0 / 5.0'),
        ('4.5 / 5.0', '4.5 / 5.0'),
        ('5.0 / 5.0', '5.0 / 5.0')
    )

    like_choices = (
        ('YES', 'YES'),
        ('NO', 'NO')
    )
    author = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.CharField(max_length=10, choices=rating_choices)
    like = models.CharField(max_length=3, choices=like_choices)
    date = models.DateTimeField(auto_now_add=True)
    cover_art_url = models.CharField(max_length=500)
    album_id = models.CharField(max_length=62)
    artist_id = models.CharField(max_length=62)

    def __str__(self):
        return f"USER: {self.author}.....Album: {self.album}.....Artist: {self.artist}.....Rating: {self.rating}.....Like?: {self.like}.....Date: {self.date}"

    # Function to show a snippet of the review for certain pages
    def shorten(self):
        if len(self.text) > 250:
            return self.text[:250] + "..."
        # Don't add the '...' if the entire review is being displayed
        else:
            return self.text
