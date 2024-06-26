from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from igdb.main.models import Profile

user_model = get_user_model()
profile_model = Profile


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput,
    )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = user_model
        fields = ['username', 'email']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        Profile.objects.create(user=user)


"""
Since we are using the built-in User model we have to define our Profile fields manually.
"""


class UpdateUserForm(forms.ModelForm):
    avatar = forms.URLField(
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )

    country = forms.CharField(
        max_length=50,
        required=False,
    )

    birthdate = forms.DateField(
        required=False,
    )

    class Meta:
        model = user_model
        fields = ["first_name", "last_name", "email"]

        help_texts = {
            "description": "Enter a short description of your profile.",
            "birthdate": "Enter your birthdate in YYYY-MM-DD format.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = self.instance.profile
        self.fields['avatar'].initial = profile.avatar
        self.fields['description'].initial = profile.description
        self.fields['country'].initial = profile.country
        self.fields['birthdate'].initial = profile.birthdate

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)

            profile.avatar = self.cleaned_data['avatar']
            profile.description = self.cleaned_data['description']
            profile.country = self.cleaned_data['country']
            profile.birthdate = self.cleaned_data['birthdate']
            profile.save()

        return user
