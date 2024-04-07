from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View

from igdb.main.forms import CreateUserForm, UserLoginForm, UpdateUserForm
from igdb.main.models import Profile


# Create your views here.
user_model = get_user_model()


class HomeView(View):
    def get(self, request):
        return render(request, template_name="home.html")


def sign_in(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
    else:
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
        user = Profile.objects.get(id=pk)
        return render(request, template_name="main\\read_user.html", context={"user": user})


class UpdateUserView(LoginRequiredMixin, View):
    model = Profile
    template_name = "main\\update_user.html"
    login_url = reverse_lazy("sign_in")

    def get(self, request, pk):
        user = user_model.objects.get(id=pk)
        form = UpdateUserForm(instance=user)

        if request.user != user:
            return redirect("update_user", pk=request.user.id)

        return render(request, template_name=self.template_name, context={"user": user, "form": form})

    def post(self, request, pk):
        profile = Profile.objects.get(id=pk)
        user1 = user_model.objects.get(id=pk)
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
