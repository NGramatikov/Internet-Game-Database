from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView

from igdb.games.models import VideoGame, NonVideoGame
from igdb.games.views import ReadGameView
from igdb.interaction.forms import CreateCuratedListForm, CreateReviewForm, UpdateReviewForm, UpdateCuratedListForm
from igdb.interaction.models import Review, CuratedList


# Create your views here.

class CuratedListsView(View):
    model = CuratedList

    def get(self, request):
        context = {"curated_list": self.model.objects.all()}
        return render(request, context=context, template_name="curated_lists.html")


class ReviewsView(View):
    model = Review

    def get(self, request):
        context = {"reviews": Review.objects.all()}
        return render(request, context=context, template_name="reviews.html")


class CreateCuratedListView(CreateView):
    model = CuratedList
    form_class = CreateCuratedListForm
    template_name = "interaction\\create_list.html"

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


class UpdateCuratedListView(View):
    def get(self, request, slug):
        curated_list = get_object_or_404(CuratedList, slug=slug)
        form = UpdateCuratedListForm(instance=curated_list)
        return render(request, template_name="interaction\\update_list.html", context={"form": form})

    def post(self, request, slug):
        curated_list = get_object_or_404(CuratedList, slug=slug)
        form = CreateCuratedListForm(request.POST or None, instance=curated_list)

        if request.POST.get("action") == "delete":
            curated_list.delete()
            return redirect("home")

        if form.is_valid():
            form.save()
            return redirect(f"/list/{curated_list.slug}/")
        return render(request, template_name="interaction\\update_list.html", context={"form": form})


class CreateReviewView(CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = "interaction\\create_review.html"

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


class UpdateReviewView(View):
    def get(self, request, slug):
        review = get_object_or_404(Review, slug=slug)
        form = UpdateReviewForm(instance=review)
        return render(request, template_name="interaction\\update_review.html", context={"form": form})

    def post(self, request, slug):
        review = get_object_or_404(Review, slug=slug)
        form = CreateReviewForm(request.POST or None, instance=review)

        if request.POST.get("action") == "delete":
            review.delete()
            return redirect("home")

        if form.is_valid():
            form.save()
            return redirect(f"/review/{review.slug}/")
        return render(request, template_name="interaction\\update_review.html", context={"form": form})
