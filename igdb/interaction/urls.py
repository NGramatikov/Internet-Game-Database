from django.urls import path

from igdb.interaction.views import (CuratedListsView, ReviewsView, CreateListView, ReadListView, UpdateListView,
                                    CreateReviewView, ReadReviewView, UpdateReviewView)

urlpatterns = [path("lists/", CuratedListsView.as_view(), name="curated_lists"),
               path("reviews/", ReviewsView.as_view(), name="reviews"),
               path("list/create/", CreateListView.as_view(), name="create_list"),
               path("list/<int:pk>/", ReadListView.as_view(), name="read_list"),
               path("list/<int:pk>/update/", UpdateListView.as_view(), name="update_list"),
               path("review/create/", CreateReviewView.as_view(), name="create_review"),
               path("review/<int:pk>/", ReadReviewView.as_view(), name="read_review"),
               path("review/<int:pk>/update/", UpdateReviewView.as_view(), name="update_review")]
