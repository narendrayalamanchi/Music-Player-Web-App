from django.db import models
from authentication.models import Users
from datetime import datetime
import os

def song_thumbnail_uploadpath(instance, filename):
    filename = os.path.basename(filename)
    return f'{instance.language}/thumbnails/{datetime.now().strftime("%Y%m%d")}_{filename}'
def song_uploadpath(instance, filename):
    filename = os.path.basename(filename)
    return f'{instance.language}/songs/{datetime.now().strftime("%Y%m%d")}_{filename}'

# Create your models here.
class Song(models.Model):
    Language_Choice = (
        ("Telugu", "Telugu"),
        ("Hindi", "Hindi"),
        ("English", "English")
    )
    name = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    language = models.CharField(max_length=25, choices=Language_Choice, default="Telugu")
    song_thumbnail = models.FileField(upload_to=song_thumbnail_uploadpath)
    year = models.IntegerField()
    singer = models.CharField(max_length=100)
    song_file = models.FileField(upload_to=song_uploadpath)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Song'

class Playlist(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=100)
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Playlist'