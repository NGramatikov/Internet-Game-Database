from django.urls import path

from igdb.games.views import GamesView, CreateGameView, ReadGameView, UpdateGameView

urlpatterns = [path("games/", GamesView.as_view(), name="games"),
               path("game/create/", CreateGameView.as_view(), name="create_game"),
               path("game/<str:slug>/", ReadGameView.as_view(), name="read_game"),
               path("game/<str:slug>/update/", UpdateGameView.as_view(), name="update_game")]
