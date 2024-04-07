from django import forms

from igdb.games.models import VideoGame, NonVideoGame


# We need to check what type of game the user chooses so we can use the appropriate form. This is done via JavaScript in
# the template games\\create. We also need to add a user as only the user who creates a game object can later update or
# delete it. We also need to override the save method to include the user otherwise we will get an ValidationError:
# {'user': ['This field cannot be null.']}

class CreateVideoGameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(CreateVideoGameForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].required = False
        # self.fields["user"].initial = user

    def save(self, commit=True):
        instance = super(CreateVideoGameForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = VideoGame
        fields = ["user", "name", "age_range", "release_year", "developer", "publisher"]
        error_messages = {"name": {"unique": "A video game with that name already exists."}}
        help_texts = {"age_range": "Please enter the recommended minimum age to play this game."}

    # def clean(self):
    #     cleaned_data = super().clean()
    #     cleaned_data.pop("user", None)
    #     return cleaned_data


class CreateNonVideoGameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(CreateNonVideoGameForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].required = False
        # self.fields["user"].initial = user
        self.fields["type"] = forms.ChoiceField(choices=(("Party Games", "Party Games"),
                                                         ("Tabletop Games", "Tabletop Games"),
                                                         ("Other Games", "Other Games"),))

    def save(self, commit=True):
        instance = super(CreateNonVideoGameForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = NonVideoGame
        fields = ["user", "name", "type", "age_range", "players", "rules", "chance"]
        error_messages = {"name": {"unique": "A video game with that name already exists."}}
        help_texts = {"players": "Please enter the minimum number of players."}

    # def clean(self):
    #     cleaned_data = super().clean()
    #     cleaned_data.pop("user", None)
    #     return cleaned_data


class UpdateVideoGameForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        exclude = ["user", "name", "slug", "type"]
        help_texts = {"cover": "Please select a cover image.",
                      "trailer": "You can enter a Youtube link to the trailer here.",
                      "gameplay": "You can enter a Youtube link to the gameplay here."}


class UpdateNonVideoGameForm(forms.ModelForm):
    class Meta:
        model = NonVideoGame
        exclude = ["user", "name", "slug", "type"]
        widgets = {"setup_time": forms.TimeInput(format="%H:%M"),
                   "playtime": forms.TimeInput(format="%H:%M")}
        help_texts = {"setup_time": "How long does it take to setup the game in format HH:MM.",
                      "playtime": "How long does it take to play the game in format HH:MM.",
                      "skills": "Does the game require any particular skills?"}
