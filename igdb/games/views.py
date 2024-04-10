from itertools import chain
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from utils import get_game_object, extract_youtube_id
from igdb.games.models import VideoGame, NonVideoGame
from igdb.interaction.models import Review, CuratedList
from igdb.games.forms import CreateVideoGameForm, CreateNonVideoGameForm, UpdateVideoGameForm, UpdateNonVideoGameForm


# Create your views here.
class GamesView(View):
    def get(self, request):
        # video_games = VideoGame.objects.all()
        # non_video_games = NonVideoGame.objects.all()
        all_games = list(chain(VideoGame.objects.all(), NonVideoGame.objects.all()))

        video_games = VideoGame.objects.order_by('?')[:10]
        non_video_games = NonVideoGame.objects.order_by('?')[:10]
        curated_lists = CuratedList.objects.order_by('?')[:10]
        reviews = Review.objects.order_by('?')[:10]

        context = {"video_games": video_games, "non_video_games": non_video_games, "all_games": all_games,
                   "curated_lists": curated_lists, "reviews": reviews}

        return render(request, template_name="games.html", context=context)


"""
By using the LoginRequiredMixin we make sure that only authenticated users can create, update or delete games. Otherwise
we redirect them to the login page. We also make sure to add the user field to the form kwargs and save him when the 
form is valid so that the actual user doesn't have to. 
"""


class CreateGameView(LoginRequiredMixin, CreateView):
    video_game_form_class = CreateVideoGameForm
    non_video_game_form_class = CreateNonVideoGameForm
    login_url = reverse_lazy("sign_in")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get(self, request, *args, **kwargs):
        video_game_form = self.video_game_form_class(user=request.user)
        non_video_game_form = self.non_video_game_form_class(user=request.user)
        context = {"video_game_form": video_game_form, "non_video_game_form": non_video_game_form}

        return render(request, template_name="games\\create_game.html", context=context)

    def post(self, request, *args, **kwargs):
        video_game_form = self.video_game_form_class(request.POST or None, user=request.user)
        non_video_game_form = self.non_video_game_form_class(request.POST or None, user=request.user)

        if request.method == "POST" and video_game_form.is_valid():
            video_game = video_game_form.save()
            slug = video_game.slug
            return redirect(reverse("read_game", kwargs={"slug": slug}))

        elif request.method == "POST" and non_video_game_form.is_valid():
            non_video_game = non_video_game_form.save()
            slug = non_video_game.slug
            return redirect(reverse("read_game", kwargs={"slug": slug}))

        else:
            context = {"video_game_form": video_game_form, "non_video_game_form": non_video_game_form}
            return render(request, template_name="games\\create_game.html", context=context)


"""
Since the games are in two different database tables their ids will duplicate, so we will identify them by slug to make
sure we have the right object. Also this code repeats itself several times across the project so we might as well make
it a separate function which can be imported into other files.
"""


class ReadGameView(View):
    video_game_model = VideoGame
    non_video_game_model = NonVideoGame

    def get(self, request, slug):
        game = get_game_object(slug)
        game_content_type = ContentType.objects.get_for_model(game)
        ratings = game.ratings.all()
        likes = game.likes.all()
        comments = game.comments.all()
        reviews = game.reviews.all()

        if game.trailer:
            trailer_id = extract_youtube_id(game.trailer)
        else:
            trailer_id = None

        if game.gameplay:
            gameplay_id = extract_youtube_id(game.gameplay)
        else:
            gameplay_id = None

        if ratings:
            avg_rating = sum([el.content for el in ratings]) / len(ratings)
        else:
            avg_rating = 0

        if request.user.is_authenticated:
            is_liked = likes.filter(user=request.user).exists()
            is_rated = ratings.filter(user=request.user).exists()
            rating = ratings.filter(user=request.user).first()
            is_commented = comments.filter(user=request.user).exists()
            is_reviewed = (Review.objects.filter(user=request.user, content_type=game_content_type,
                                                 object_id=game.id).exists())

            if is_reviewed:
                review_slug = (Review.objects.filter(user=request.user, content_type=game_content_type,
                                                     object_id=game.id).first().slug)
            else:
                review_slug = None

        else:
            is_liked = False
            is_rated = False
            is_reviewed = False
            is_commented = False
            rating = 0
            review_slug = None

        context = {"game": game, "ratings": ratings, "likes": likes, "comments": comments, "reviews": reviews,
                   "is_liked": is_liked, "is_rated": is_rated, "avg_rating": avg_rating, "rating": rating,
                   "is_commented": is_commented, "is_reviewed": is_reviewed, "review_slug": review_slug,
                   "trailer_id": trailer_id, "gameplay_id": gameplay_id}

        return render(request, template_name="games\\read_game.html", context=context)


"""
If the user is not logged in we redirect him to the read_game page. We also make sure to add the user field to the form 
kwargs and save him when the form is valid. We also make sure the game is deleted when the user presses the delete 
button and confirms the action. That kind of violates the single responsibility principle, but most real web pages allow
to modify and delete an object on the same page.
"""


class UpdateGameView(LoginRequiredMixin, View):
    template_name = "games\\update_game.html"
    login_url = reverse_lazy("sign_in")

    def get(self, request, slug):
        game = get_game_object(slug)

        if request.user != game.user:
            return redirect("read_game", slug=slug)

        if isinstance(game, VideoGame):
            form = UpdateVideoGameForm(instance=game)
        else:
            form = UpdateNonVideoGameForm(instance=game)

        return render(request, self.template_name, {"game": game, "form": form})

    def post(self, request, slug):
        game = get_game_object(slug)

        if request.user != game.user:
            return redirect("read_game", slug=slug)

        if isinstance(game, VideoGame):
            form = UpdateVideoGameForm(request.POST, instance=game)
        else:
            form = UpdateNonVideoGameForm(request.POST, instance=game)

        if request.POST.get("action") == "delete":
            game.delete()
            return redirect("home")

        if form.is_valid():
            form.save()
            return redirect("read_game", slug=slug)

        return render(request, self.template_name, {"game": game, "form": form})
