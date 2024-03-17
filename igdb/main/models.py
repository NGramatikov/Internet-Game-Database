from django.db import models
from django.contrib.auth.models import User
# from igdb.games.models import CuratedList
# from igdb.interaction.models import Review, Like, Comment
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    avatar = models.ImageField()
    description = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    # curated_lists = models.ForeignKey("games.CuratedList", on_delete=models.DO_NOTHING)
    # reviews = models.ForeignKey("interaction.Review", on_delete=models.DO_NOTHING)
    # likes = models.ForeignKey("interaction.Like", on_delete=models.DO_NOTHING)
    # comments = models.ForeignKey("interaction.Comment", on_delete=models.DO_NOTHING)
