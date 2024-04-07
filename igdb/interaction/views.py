from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from igdb.games.models import VideoGame, NonVideoGame
from igdb.games.views import ReadGameView
from igdb.interaction.forms import CreateCuratedListForm, CreateReviewForm, UpdateReviewForm, UpdateCuratedListForm, \
    CreateLikeForm, CreateCommentForm, CreateRatingForm, UpdateCommentForm, UpdateRatingForm, DeleteLikeForm
from igdb.interaction.models import Review, CuratedList, Like, Comment, Rating


# Create your views here.

class CuratedListsView(View):
    model = CuratedList

    def get(self, request):
        context = {"curated_lists": self.model.objects.all()}
        return render(request, context=context, template_name="curated_lists.html")


class ReviewsView(View):
    model = Review

    def get(self, request):
        context = {"reviews": Review.objects.all()}
        return render(request, context=context, template_name="reviews.html")


class CreateCuratedListView(LoginRequiredMixin, CreateView):
    model = CuratedList
    form_class = CreateCuratedListForm
    template_name = "interaction\\create_list.html"
    login_url = reverse_lazy("sign_in")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse("read_list", kwargs={"slug": self.object.slug})


class ReadCuratedListView(View):
    def get(self, request, slug):
        curated_list = CuratedList.objects.get(slug=slug)
        context = {"curated_list": curated_list}
        return render(request, "interaction\\read_list.html", context)


class UpdateCuratedListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("sign_in")

    def get(self, request, slug):
        curated_list = get_object_or_404(CuratedList, slug=slug)
        form = UpdateCuratedListForm(instance=curated_list)

        if request.user != curated_list.user:
            return redirect("read_list", slug=slug)

        return render(request, template_name="interaction\\update_list.html", context={"form": form})

    def post(self, request, slug):
        curated_list = get_object_or_404(CuratedList, slug=slug)
        form = CreateCuratedListForm(request.POST or None, instance=curated_list)

        if request.user != curated_list.user:
            return redirect("read_list", slug=slug)

        if request.POST.get("action") == "delete":
            curated_list.delete()
            return redirect("home")

        if form.is_valid():
            form.save()
            return redirect(f"/list/{curated_list.slug}/")
        return render(request, template_name="interaction\\update_list.html", context={"form": form})


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = "interaction\\create_review.html"
    login_url = reverse_lazy("sign_in")

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            game = VideoGame.objects.get(slug=slug)
            return game
        except VideoGame.DoesNotExist:
            game = NonVideoGame.objects.get(slug=slug)
            return game

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["object_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        game = self.get_object()
        form.instance.content_object = game
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse("read_review", kwargs={"slug": self.object.slug})


class ReadReviewView(View):
    model = Review

    def get(self, request, slug):
        review = Review.objects.get(slug=slug)
        return render(request, template_name="interaction\\read_review.html", context={"review": review})


class UpdateReviewView(LoginRequiredMixin, View):
    login_url = reverse_lazy("sign_in")

    def get(self, request, slug):
        review = get_object_or_404(Review, slug=slug)
        form = UpdateReviewForm(instance=review)
        if request.user != review.user:
            return redirect("read_review", slug=slug)
        return render(request, template_name="interaction\\update_review.html", context={"form": form})

    def post(self, request, slug):
        review = get_object_or_404(Review, slug=slug)
        form = CreateReviewForm(request.POST or None, instance=review)

        if request.user != review.user:
            return redirect("read_review", slug=slug)

        if request.POST.get("action") == "delete":
            review.delete()
            return redirect("home")

        if form.is_valid():
            form.save()
            return redirect(f"/review/{review.slug}/")

        return render(request, template_name="interaction\\update_review.html", context={"form": form})


class CreateLikeView(LoginRequiredMixin, View):
    login_url = reverse_lazy("sign_in")

    def post(self, request, slug):
        try:
            game = VideoGame.objects.get(slug=slug)
        except VideoGame.DoesNotExist:
            game = NonVideoGame.objects.get(slug=slug)
        form = CreateLikeForm(request.POST)
        if form.is_valid():
            like = form.save(commit=False)
            like.user = request.user
            like.content_object = game
            like.save()
            return redirect("read_game", slug=game.slug)
        return redirect("read_game", slug=game.slug)


class DeleteLikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        try:
            game = VideoGame.objects.get(slug=slug)
        except VideoGame.DoesNotExist:
            game = NonVideoGame.objects.get(slug=slug)

        like = Like.objects.filter(user=request.user, object_id=game.id)

        if like:
            like.delete()

        return redirect(reverse("read_game", kwargs={"slug": slug}))


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CreateCommentForm
    template_name = "interaction\\create_comment.html"
    login_url = reverse_lazy("sign_in")

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            game = VideoGame.objects.get(slug=slug)
            return game
        except VideoGame.DoesNotExist:
            game = NonVideoGame.objects.get(slug=slug)
            return game

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["object_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        game = self.get_object()
        form.instance.content_object = game
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        game = self.get_object()
        return reverse("read_game", kwargs={"slug": game.slug})


class UpdateCommentView(LoginRequiredMixin, View):
    login_url = reverse_lazy("sign_in")

    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        form = UpdateCommentForm(instance=comment)

        if request.user != comment.user:
            return redirect("read_game", slug=comment.content_object.slug)

        return render(request, template_name="interaction\\update_comment.html", context={"form": form})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        form = CreateCommentForm(request.POST or None, instance=comment)
        slug = comment.content_object.slug

        if request.user != comment.user:
            return redirect("read_game", slug=slug)

        if request.POST.get("action") == "delete":
            comment.delete()
            return redirect("read_game", slug)

        if form.is_valid():
            form.save()
            return redirect("read_game", slug)

        return render(request, template_name="interaction\\update_comment.html", context={"form": form})


class CreateRatingView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = CreateRatingForm
    template_name = "interaction\\create_rating.html"
    login_url = reverse_lazy("sign_in")

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            game = VideoGame.objects.get(slug=slug)
            return game
        except VideoGame.DoesNotExist:
            game = NonVideoGame.objects.get(slug=slug)
            return game

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["object_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        game = self.get_object()
        form.instance.content_object = game
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        game = self.get_object()
        return reverse("read_game", kwargs={"slug": game.slug})


class UpdateRatingView(LoginRequiredMixin, View):
    login_url = reverse_lazy("sign_in")

    def get(self, request, pk):
        rating = get_object_or_404(Rating, id=pk)
        form = UpdateRatingForm(instance=rating)

        if request.user != rating.user:
            return redirect("read_game", slug=rating.content_object.slug)

        return render(request, template_name="interaction\\update_rating.html", context={"form": form})

    def post(self, request, pk):
        rating = get_object_or_404(Rating, id=pk)
        form = CreateCommentForm(request.POST or None, instance=rating)
        slug = rating.content_object.slug

        if request.user != rating.user:
            return redirect("read_game", slug=rating.content_object.slug)

        if request.POST.get("action") == "delete":
            rating.delete()
            return redirect("read_game", slug)

        if form.is_valid():
            form.save()
            return redirect("read_game", slug)

        return render(request, template_name="interaction\\update_rating.html", context={"form": form})
