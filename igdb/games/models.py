from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.core.validators import MinLengthValidator

from igdb.main.models import Profile
from igdb.games.validators import validate_name
from igdb.interaction.models import Rating, Like, Comment, Rateable, Likeable, Commentable, Reviewable

# Create your models here.

GAME_TYPES = (("Party Games", "Party Games"),
              ("Tabletop Games", "Tabletop Games"),
              ("Video Games", "Video Games"),
              ("Other Games", "Other Games"),)

AGE_RANGE = [(i, i) for i in range(1, 19)]

RELEASE_YEARS = [(i, i) for i in range(1958, datetime.now().year + 5)]

CHANCE = (("Low", "Low"),
          ("Medium", "Medium"),
          ("High", "High"),
          ("Not applicable", "Not applicable"),)

user_model = get_user_model()


# We create the parent class for all games. If we don't set the default type to Video Games we will get an
# {'type': ['This field cannot be blank.']}" error when trying to create a VideoGame object. It didn't matter if we set
# the type to initial="Video Games" in the form.
class Game(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(to=user_model, on_delete=models.DO_NOTHING, null=False, blank=False)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, validators=[validate_name])
    description = models.TextField(blank=True, null=True, validators=[MinLengthValidator(20)])
    type = models.CharField(max_length=50, choices=GAME_TYPES, null=False, blank=False, default="Video Games")
    genre = models.CharField(max_length=50, blank=True, null=True)
    age_range = models.PositiveSmallIntegerField(choices=AGE_RANGE, null=False, blank=False)
    cover = models.ImageField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    # When saving an object Django doesn't call the validators, so we add full_clean. If we want the slug to contain
    # a primary key we have to save the object first.
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.name[:10]}-{self.pk}")
            super().save(*args, **kwargs)


class VideoGame(Game, Likeable, Rateable, Commentable, Reviewable):
    release_year = models.PositiveSmallIntegerField(choices=RELEASE_YEARS, null=False, blank=False)
    trailer = models.URLField(blank=True, null=True)
    gameplay = models.URLField(blank=True, null=True)
    developer = models.CharField(max_length=100, blank=False, null=False)
    publisher = models.CharField(max_length=100, blank=False, null=False)
    system_requirements = models.TextField(blank=True, null=True, validators=[MinLengthValidator(20)])

    def __str__(self):
        return f"{self.name} was released in {self.release_year} by {self.publisher}."


# TODO: fix the time so it can keep more than 12 hours
class NonVideoGame(Game, Likeable, Rateable, Commentable, Reviewable):
    players = models.PositiveSmallIntegerField(null=False, blank=False)
    rules = models.TextField(null=False, blank=False)
    setup_time = models.TimeField(blank=True, null=True)
    playtime = models.TimeField(blank=True, null=True)
    chance = models.CharField(choices=CHANCE, blank=False, null=False)
    skills = models.CharField(max_length=200, blank=True, null=True, validators=[MinLengthValidator(20)])

    def __str__(self):
        return f"{self.name} is played by {self.players} and involves {self.chance} chance."
