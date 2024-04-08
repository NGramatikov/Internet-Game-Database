from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View, CreateView
from igdb.games.models import VideoGame, NonVideoGame
from igdb.interaction.models import Review, CuratedList, Like, Comment, Rating
from igdb.interaction.forms import (CreateCuratedListForm, CreateReviewForm, UpdateReviewForm, UpdateCuratedListForm,
                                    CreateLikeForm, CreateCommentForm, CreateRatingForm, UpdateCommentForm,
                                    UpdateRatingForm)
from utils import get_game_object

# Create your views here.

'''
I noticed this code repeating itself so here we are again. This particular snippet gets the game object, assigns the 
user to the form kwargs and on successful validation assigns the user to the game object.
'''


class CreateGenericInteractionView(LoginRequiredMixin, CreateView):
    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        game = get_game_object(slug)
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


class CuratedListsView(View):
    model = CuratedList

    def get(self, request):
        context = {"curated_lists": self.model.objects.all()}
        return render(request, template_name="curated_lists.html", context=context)


class ReviewsView(View):
    model = Review

    def get(self, request):
        context = {"reviews": Review.objects.all()}
        return render(request, template_name="reviews.html", context=context)


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
        curated_list = get_object_or_404(CuratedList, slug=slug)
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


class CreateReviewView(CreateGenericInteractionView):
    model = Review
    form_class = CreateReviewForm
    template_name = "interaction\\create_review.html"
    login_url = reverse_lazy("sign_in")

    def get_success_url(self):
        return reverse("read_review", kwargs={"slug": self.object.slug})


class ReadReviewView(View):
    def get(self, request, slug):
        review = get_object_or_404(Review, slug=slug)
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
        game = get_game_object(slug)
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
        game = get_game_object(slug)
        like = Like.objects.filter(user=request.user, object_id=game.id)

        if like:
            like.delete()

        return redirect(reverse("read_game", kwargs={"slug": slug}))


class CreateCommentView(CreateGenericInteractionView):
    model = Comment
    form_class = CreateCommentForm
    template_name = "interaction\\create_comment.html"
    login_url = reverse_lazy("sign_in")

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


class CreateRatingView(CreateGenericInteractionView):
    model = Rating
    form_class = CreateRatingForm
    template_name = "interaction\\create_rating.html"
    login_url = reverse_lazy("sign_in")

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
