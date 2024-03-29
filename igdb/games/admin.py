from django.contrib import admin
from igdb.games.models import VideoGame, NonVideoGame


# Register your models here.

@admin.register(VideoGame)
class VideoGameAdmin(admin.ModelAdmin):
    list_display = ("name", "release_year", "developer")


@admin.register(NonVideoGame)
class NonVideoGameAdmin(admin.ModelAdmin):
    list_display = ("name", "players", "chance")
