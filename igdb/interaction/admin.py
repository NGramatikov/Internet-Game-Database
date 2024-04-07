from django.contrib import admin
from igdb.interaction.models import Like, Comment, Rating, Review, CuratedList

# Register your models here.


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "content_object")
    list_filter = ("user",)
    ordering = ("user",)
    search_fields = ("user",)
    readonly_fields = ("user",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content_object", "content")
    list_filter = ("user",)
    ordering = ("user",)
    search_fields = ("user",)
    readonly_fields = ("user",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "content_object", "content")
    list_filter = ("user",)
    ordering = ("user", "content")
    search_fields = ("user", "content")
    readonly_fields = ("user",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "slug", "content_object")
    list_filter = ("user",)
    ordering = ("user", "title")
    search_fields = ("user",)
    readonly_fields = ("user", "title", "slug")


@admin.register(CuratedList)
class CuratedListAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "slug")
    list_filter = ("user",)
    ordering = ("user", "title")
    search_fields = ("user",)
    readonly_fields = ("user", "title")
