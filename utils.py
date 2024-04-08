from django.contrib.contenttypes.models import ContentType
from django import forms
from django.http import HttpResponseNotFound
from igdb.games.models import VideoGame, NonVideoGame
'''
I noticed certain code snippets repeat themselves over and over so I put them here so they can be imported and reused
in other files.
'''


def get_game_object(slug):
    try:
        game = VideoGame.objects.get(slug=slug)
        return game
    except VideoGame.DoesNotExist:
        game = NonVideoGame.objects.get(slug=slug)
        return game
    except NonVideoGame.DoesNotExist:
        return HttpResponseNotFound("Game does not exist")
