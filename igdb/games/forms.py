from django import forms

from igdb.games.models import VideoGame, NonVideoGame

"""
We need to check what type of game the user chooses so we can use the appropriate form. This is done in the template
'games\\create_game.html'. We also need to add a user as only the user who creates a game object can later update or
delete it. We also need to override the save method to include the user otherwise we will get a ValidationError:
{'user': ['This field cannot be null.']} If we don't change user.required to False we won't be able to submit the form.
"""


class CreateVideoGameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(CreateVideoGameForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].required = False

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


"""
We need to exclude "Video Games" from the "type" ChoiceField as those are dealt with the other form.
"""


class CreateNonVideoGameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(CreateNonVideoGameForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].required = False

        self.fields["type"] = forms.ChoiceField(choices=
                                                (("Party Games", "Party Games"),
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


"""
We exclude the user, name and slug fields from the form as those are unique identifiers and shouldn't be changed.
And it's extremely rare for a game to change its type.
"""


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
