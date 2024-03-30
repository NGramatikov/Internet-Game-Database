from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from igdb.games.forms import CreateVideoGameForm, CreateNonVideoGameForm, UpdateVideoGameForm, UpdateNonVideoGameForm
from igdb.games.models import VideoGame, NonVideoGame, Game


# Create your views here.
class GamesView(View):
    video_game_model = VideoGame
    non_video_game_model = NonVideoGame

    def get(self, request):
        games = {"video_games": VideoGame.objects.all(), "non_video_games": NonVideoGame.objects.all()}
        return render(request, context=games, template_name="games.html")


class CreateGameView(View):
    video_game_form_class = CreateVideoGameForm
    non_video_game_form_class = CreateNonVideoGameForm
    template_name = "games/create_game.html"
    success_url = "/"

    def get(self, request):
        video_game_form = self.video_game_form_class()
        non_video_game_form = self.non_video_game_form_class()
        context = {"video_game_form": video_game_form, "non_video_game_form": non_video_game_form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        video_game_form = self.video_game_form_class(request.POST or None)
        non_video_game_form = self.non_video_game_form_class(request.POST or None)

        if request.method == "POST" and video_game_form.is_valid():
            video_game_form.save()
            return redirect(self.success_url)
        elif request.method == "POST" and non_video_game_form.is_valid():
            non_video_game_form.save()
            return redirect(self.success_url)
        else:
            context = {"video_game_form": video_game_form, "non_video_game_form": non_video_game_form}
            return render(request, template_name=self.template_name, context=context)


# Since the games are in two different database tables their ids will duplicate, so we will identify them by slug.
class ReadGameView(View):
    video_game_model = VideoGame
    non_video_game_model = NonVideoGame

    def get(self, request, slug):
        try:
            game = VideoGame.objects.get(slug=slug)
        except VideoGame.DoesNotExist:
            game = NonVideoGame.objects.get(slug=slug)

        context = {"game": game}
        return render(request, template_name="games\\read_game.html", context=context)


class UpdateGameView(View):
    template_name = "games\\update_game.html"

    def get_game(self, slug):
        try:
            game_instance = VideoGame.objects.get(slug=slug)
        except VideoGame.DoesNotExist:
            try:
                game_instance = NonVideoGame.objects.get(slug=slug)
            except NonVideoGame.DoesNotExist:
                # Handle case where neither VideoGame nor NonVideoGame with the given slug exists
                pass
        return game_instance

    def get(self, request, slug):
        game_instance = self.get_game(slug)
        if isinstance(game_instance, VideoGame):
            game_form = UpdateVideoGameForm(instance=game_instance)
        else:
            game_form = UpdateNonVideoGameForm(instance=game_instance)
        return render(request, self.template_name, {"game_instance": game_instance, "game_form": game_form})

    def post(self, request, slug):
        game_instance = self.get_game(slug)
        if isinstance(game_instance, VideoGame):
            game_form = UpdateVideoGameForm(request.POST, instance=game_instance)
        else:
            game_form = UpdateNonVideoGameForm(request.POST, instance=game_instance)

        if request.POST.get("action") == "delete":
            game_instance.delete()
            return redirect("home")

        if game_form.is_valid():
            game_form.save()
            return redirect("read_game", slug=slug)

        return render(request, self.template_name, {"game_instance": game_instance, "game_form": game_form})
