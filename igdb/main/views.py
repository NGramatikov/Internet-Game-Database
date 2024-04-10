from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model

from igdb.main.models import Profile
from igdb.games.models import VideoGame, NonVideoGame
from igdb.interaction.models import CuratedList, Review
from igdb.main.forms import CreateUserForm, UserLoginForm, UpdateUserForm

# Create your views here.
user_model = get_user_model()


class HomeView(View):
    def get(self, request):
        video_games = VideoGame.objects.all()
        non_video_games = NonVideoGame.objects.all()
        curated_lists = CuratedList.objects.all()
        reviews = Review.objects.all()
        context = {"video_games": video_games, "non_video_games": non_video_games, "curated_lists": curated_lists,
                   "reviews": reviews}
        return render(request, template_name="home.html", context=context)


class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get('query')
        video_games = VideoGame.objects.filter(name__icontains=query)
        non_video_games = NonVideoGame.objects.filter(name__icontains=query)
        users = user_model.objects.filter(username__icontains=query)
        context = {"query": query, "video_games": video_games, "non_video_games": non_video_games, "users": users}
        print(context)

        return render(request, template_name="search_results.html", context=context)


def sign_in(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect("home")

        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        if request.user.is_authenticated:
            return redirect("home")
        form = UserLoginForm()

    return render(request, "main\\signin.html", {"form": form})


class SignOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("sign_in")


class CreateUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        form = CreateUserForm()
        context = {"form": form}

        return render(request, "main\\create_user.html", context=context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        form = CreateUserForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            form.save()
            return redirect("sign_in")
        else:
            form = CreateUserForm()
            context = {"form": form}

        return render(request, "main\\create_user.html", context=context)


class ReadUserView(View):
    model = Profile

    def get(self, request, pk):
        user = get_object_or_404(Profile, id=pk)

        reviews = user.user.review_set.all()
        comments = user.user.comment_set.all()
        ratings = user.user.rating_set.all()
        likes = user.user.like_set.all()
        video_games = user.user.videogame_set.all()
        non_video_games = user.user.nonvideogame_set.all()

        context = {"user": user, "reviews": reviews, "comments": comments, "ratings": ratings, "likes": likes,
                   "video_games": video_games, "non_video_games": non_video_games}

        return render(request, template_name="main\\read_user.html", context=context)


class UpdateUserView(LoginRequiredMixin, View):
    model = Profile
    template_name = "main\\update_user.html"
    login_url = reverse_lazy("sign_in")

    def get(self, request, pk):
        user = get_object_or_404(user_model, id=pk)
        form = UpdateUserForm(instance=user)

        if request.user != user:
            return redirect("update_user", pk=request.user.id)

        return render(request, template_name=self.template_name, context={"user": user, "form": form})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, id=pk)
        user1 = get_object_or_404(user_model, id=pk)
        form = UpdateUserForm(request.POST, instance=user1)

        if request.user != user1:
            return redirect("update_user", pk=request.user.id)

        if request.POST.get("action") == "delete":
            if request.user.is_authenticated:
                logout(request)
            user1.delete()
            return redirect("home")

        if form.is_valid():
            form.save()
            return redirect("read_user", pk=pk)

        return render(request, self.template_name, context={"user": profile, "form": form})
