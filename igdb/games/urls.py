from django.urls import path

from igdb.games.views import GamesView, CreateGameView, ReadGameView, UpdateGameView
from igdb.interaction.views import CreateReviewView, CreateLikeView, CreateCommentView, CreateRatingView, DeleteLikeView

urlpatterns = [path("games/", GamesView.as_view(), name="games"),
               path("game/create/", CreateGameView.as_view(), name="create_game"),
               path("game/<slug:slug>/", ReadGameView.as_view(), name="read_game"),
               path("game/<slug:slug>/update/", UpdateGameView.as_view(), name="update_game"),
               path("game/<slug:slug>/create_review", CreateReviewView.as_view(), name="create_review"),
               path("game/<slug:slug>/create_like", CreateLikeView.as_view(), name="create_like"),
               path("game/<slug:slug>/delete_like", DeleteLikeView.as_view(), name="delete_like"),
               path("game/<slug:slug>/create_comment", CreateCommentView.as_view(), name="create_comment"),
               path("game/<slug:slug>/create_rating", CreateRatingView.as_view(), name="create_rating")]
