from django.contrib import admin
from igdb.games.models import VideoGame, NonVideoGame


# Register your models here.

@admin.register(VideoGame)
class VideoGameAdmin(admin.ModelAdmin):
    list_display = ("name", "release_year", "developer", "age_range")
    list_select_related = ("user",)
    list_filter = ("developer", "age_range")
    ordering = ("name", "release_year")
    search_fields = ("name", "release_year")
    readonly_fields = ("user", "slug")


@admin.register(NonVideoGame)
class NonVideoGameAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "players", "chance")
    list_select_related = ("user",)
    list_filter = ("type", "age_range", "chance")
    ordering = ("name", "players")
    search_fields = ("name", "type")
    readonly_fields = ("user", "slug")
