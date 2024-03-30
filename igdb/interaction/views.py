from django.shortcuts import render
from django.views.generic import View, CreateView

from igdb.interaction.forms import CreateCuratedListForm
from igdb.interaction.models import Review, CuratedList


# Create your views here.

class CuratedListsView(View):
    model = CuratedList

    def get(self, request):
        context = {"curated_lists": CuratedList.objects.all()}
        return render(request, context=context, template_name="curated_lists.html")


class ReviewsView(View):
    model = Review

    def get(self, request):
        context = {"reviews": Review.objects.all()}
        return render(request, context=context, template_name="reviews.html")


class CreateListView(CreateView):
    model = CuratedList
    form_class = CreateCuratedListForm
    template_name = "interaction\\create_list.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReadListView(View):
    model = CuratedList

    def get(self, request, pk):
        curated_list = CuratedList.objects.get(id=pk)
        return render(request, template_name="interaction\\read_list.html")


class UpdateListView(View):
    model = CuratedList

    def get(self, request, pk):
        curated_list = CuratedList.objects.get(id=pk)
        return render(request, template_name="interaction\\update_list.html")


class CreateReviewView(View):
    def get(self, request):
        return render(request, template_name="interaction\\create_review.html")


class ReadReviewView(View):
    model = Review

    def get(self, request, pk):
        review = Review.objects.get(id=pk)
        return render(request, template_name="interaction\\read_review.html")


class UpdateReviewView(View):
    model = Review

    def get(self, request, pk):
        review = Review.objects.get(id=pk)
        return render(request, template_name="interaction\\update_review.html")
