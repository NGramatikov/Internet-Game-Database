from django.shortcuts import render
from django.views.generic import View

from igdb.main.models import Profile


# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, template_name="home.html")


class SignInView(View):
    def get(self, request):
        return render(request, template_name="main\\signin.html")


class CreateUserView(View):
    def get(self, request):
        return render(request, template_name="main\\create_user.html")


class ReadUserView(View):
    model = Profile

    def get(self, request, pk):
        user = Profile.objects.get(id=pk)
        return render(request, template_name="main\\read_user.html")


class UpdateUserView(View):
    model = Profile

    def get(self, request, pk):
        user = Profile.objects.get(id=pk)
        return render(request, template_name="main\\update_user.html")
