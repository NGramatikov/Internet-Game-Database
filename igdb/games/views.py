from django.shortcuts import render
from django.views.generic import View, CreateView

from igdb.games.forms import GameForm
from igdb.games.models import VideoGame, NonVideoGame, Game


# Create your views here.


class GamesView(View):
    video_game_model = VideoGame
    non_video_game_model = NonVideoGame

    def get(self, request):
        games = {"video_games": VideoGame.objects.all(), "non_video_games": NonVideoGame.objects.all()}
        return render(request, context=games, template_name="games.html")


class CreateGameView(CreateView):
    form_class = GameForm
    template_name = "games\\create_game.html"
    success_url = "/"


class ReadGameView(View):
    video_game_model = VideoGame
    non_video_game_model = NonVideoGame

    def get(self, request, pk):
        game = VideoGame.objects.get(id=pk)
        if not game:
            game = NonVideoGame.objects.get(id=pk)
        return render(request, template_name="games\\read_game.html")


class UpdateGameView(View):
    video_game_model = VideoGame
    non_video_game_model = NonVideoGame

    def get(self, request, pk):
        game = VideoGame.objects.get(id=pk)
        if not game:
            game = NonVideoGame.objects.get(id=pk)
        return render(request, template_name="games\\update_game.html")
