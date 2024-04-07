from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from igdb.main.models import Profile

user_model = get_user_model()
profile_model = Profile


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = user_model
        fields = ['username', 'email']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        Profile.objects.create(user=user)


class UpdateUserForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    country = forms.CharField(max_length=50, required=False)
    birthdate = forms.DateField(required=False)

    class Meta:
        model = user_model
        fields = ["first_name", "last_name", "email"]
        help_texts = {"description": "Enter a short description of your profile.",
                      "birthdate": "Enter your birthdate in YYYY-MM-DD format."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the related profile instance if it exists
        try:
            profile = self.instance.profile
            self.fields['avatar'].initial = profile.avatar
            self.fields['description'].initial = profile.description
            self.fields['country'].initial = profile.country
            self.fields['birthdate'].initial = profile.birthdate
        except Profile.DoesNotExist:
            pass

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


    # avatar = forms.ImageField(required=False)
    # description = forms.CharField(widget=forms.Textarea, required=False)
    # country = forms.CharField(max_length=50, required=False)
    # birthdate = forms.DateField(required=False)
    #
    # class Meta:
    #     model = user_model
    #     fields = ["first_name", "last_name", "email", "avatar", "description", "country", "birthdate"]
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance.profile:
    #         self.fields["avatar"].initial = self.instance.profile.avatar
    #         self.fields["description"].initial = self.instance.profile.description
    #         self.fields["country"].initial = self.instance.profile.country
    #         self.fields["birthdate"].initial = self.instance.profile.birthdate
    #
    # def save(self, commit=True):
    #     profile = self.instance.profile
    #     profile.avatar = self.cleaned_data["avatar"]
    #     profile.description = self.cleaned_data["description"]
    #     profile.country = self.cleaned_data["country"]
    #     profile.birthdate = self.cleaned_data["birthdate"]
    #
    #     if commit:
    #         profile.save()
    #     return super().save(commit)
