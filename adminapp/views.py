from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from music_dashboard.models import Song
from collections import defaultdict
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from django.core.files import File  
# Create your views here.
@staff_member_required
def extract_thumbnail_from_song(request,language):
    song_path = settings.BASE_DIR / 'mediafiles' / language.capitalize() / 'songs'
    output_dir = settings.BASE_DIR / 'mediafiles' / language.capitalize() / 'thumbnails'
    orginal_song_count = 0
    mp3_song_count = 0
    success_count = 0
    for song_file in song_path.iterdir():
        orginal_song_count += 1
        if song_file.is_file() and song_file.suffix == '.mp3': 
            mp3_song_count += 1
            audio = MP3(song_file, ID3=ID3)
            for tag in audio.tags.values():
                if isinstance(tag, APIC):  # APIC is the ID3 tag for album artwork
                    image_data = tag.data
                    image_extension = tag.mime.split('/')[1]  # Get the image extension (e.g., jpeg, png)

                    # Define output path for the extracted thumbnail
                    thumbnail_path = output_dir / f'{song_file.name.split(".")[0]}.{image_extension}'

                    # Write the image data to a file
                    with open(thumbnail_path, 'wb') as image_file:
                        image_file.write(image_data)
                    print(f'Thumbnail saved to: {thumbnail_path}')
                    success_count += 1
    
    if success_count > 0:
        return HttpResponse(f'Successfully extracted {success_count} thumbnails. Orginal Songs Count {orginal_song_count}. Mp3 Songs Count {mp3_song_count}.')
    else:
        return HttpResponse(f'No album art found in the MP3 files in {song_path}')


@staff_member_required
def add_songs(request,language):
    
    songs_dir = settings.BASE_DIR / 'mediafiles' / language.capitalize() / 'songs'
    thumbnail_dir =  settings.BASE_DIR / 'mediafiles' / language.capitalize() / 'thumbnails' 
    language = language.capitalize()
    results={'ans':[]}
    for song_file in songs_dir.iterdir():
        if song_file.is_file() and song_file.suffix == '.mp3': 
            print(song_file.name)
           
            audio = MP3(song_file, ID3=EasyID3)
            title = audio.get('title', ['Unknown Title'])[0]
            album = audio.get('album', ['Unknown Album'])[0]
            year = audio.get('date', [2010])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
            results['ans'].append( {
                'title': title,
                'album': album,
                'year': year,
                'artist': artist,
                'filename':song_file.name
            })
        
            thumbnail_extensions = ['.jpg', '.jpeg', '.png']

            song_exists = Song.objects.filter(name=title, language=language).exists()
            if not song_exists:
                with open(song_file, 'rb') as song_file_obj:
                    for ext in thumbnail_extensions:
                        thumbnail_path = thumbnail_dir / f'{song_file.name.split(".")[0]}{ext}'
                        if thumbnail_path.exists():
                            with open(thumbnail_path, 'rb') as thumb_file_obj:

                                Song.objects.create(name=title,album=album,
                                                    language=language,year=year,singer=artist,
                                                    song_file=File(song_file_obj),
                                                    song_thumbnail=File(thumb_file_obj) )
                                break
        else:
            print("Missed files of different file formats",song_file.name)

    return JsonResponse(results)
