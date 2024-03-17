from datetime import datetime
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from igdb.interaction.models import Rating, Like, Comment
from igdb.main.models import Profile

# Create your models here.

GAME_TYPES = (("Party Games", "Party Games"), ("Tabletop Games", "Tabletop Games"), ("Video Games", "Video Games"),
              ("Other Games", "Other Games"))
AGE_RANGE = [(f"{i}+", f"{i}+") for i in range(1, 19)]
RELEASE_YEARS = [(f"{i}+", f"{i}+") for i in range(1958, datetime.now().year+5)]
CHANCE = (("Low", "Low"), ("Medium", "Medium"), ("High", "High"))


class Game(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    type = models.CharField(choices=GAME_TYPES, null=False, blank=False)
    genre = models.CharField(max_length=50, null=True, blank=True)
    age_range = models.IntegerField(choices=AGE_RANGE, null=False, blank=False)
    likes = GenericRelation(Like, related_query_name='fk_game_like')
    comments = GenericRelation(Comment, related_query_name='fk_game_comment')
    ratings = GenericRelation(Rating, related_query_name='fk_game_rating')


class VideoGame(Game):
    release_year = models.IntegerField(choices=RELEASE_YEARS, null=True, blank=True)
    trailer = models.URLField(null=True, blank=True)
    gameplay = models.URLField(null=True, blank=True)
    developer = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    system_requirements = models.TextField()


class NonVideoGame(Game):
    players = models.PositiveSmallIntegerField(null=False, blank=False)
    rules = models.TextField(null=False, blank=False)
    setup_time = models.TimeField(null=True, blank=True)
    playtime = models.TimeField(null=True, blank=True)
    chance = models.CharField(choices=CHANCE, null=True, blank=True)
    skills = models.CharField(max_length=200, null=True, blank=True)


class CuratedList(models.Model):
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    games = models.ManyToManyField(to=VideoGame)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
