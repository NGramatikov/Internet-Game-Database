from django.urls import path

from igdb.interaction.views import (CuratedListsView, ReviewsView, CreateCuratedListView, ReadCuratedListView,
                                    UpdateCuratedListView, ReadReviewView, UpdateReviewView,UpdateCommentView,
                                    UpdateRatingView)

urlpatterns = [
    path("lists/", CuratedListsView.as_view(), name="curated_lists"),
    path("reviews/", ReviewsView.as_view(), name="reviews"),
    path("list/create/", CreateCuratedListView.as_view(), name="create_list"),
    path("list/<slug:slug>/", ReadCuratedListView.as_view(), name="read_list"),
    path("list/<slug:slug>/update/", UpdateCuratedListView.as_view(), name="update_list"),
    path("review/<slug:slug>/", ReadReviewView.as_view(), name="read_review"),
    path("review/<slug:slug>/update/", UpdateReviewView.as_view(), name="update_review"),
    path("comment/<int:pk>/update/", UpdateCommentView.as_view(), name="update_comment"),
    path("rating/<int:pk>/update/", UpdateRatingView.as_view(), name="update_rating"),
]
