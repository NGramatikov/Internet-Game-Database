from django import forms

from igdb.games.models import Game, GAME_TYPES, VideoGame, NonVideoGame


# We need to check what type of game the user chooses so we can use the appropriate sub-class.
class GameForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        fields = ["name", "type", "age_range"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["type"] = forms.ChoiceField(choices=GAME_TYPES)

    def save(self, commit=True):
        if self.cleaned_data["type"] == "Video Games":
            instance = VideoGame(name=self.cleaned_data["name"], type=self.cleaned_data["type"],
                                 age_range=self.cleaned_data["age_range"])
        else:
            instance = NonVideoGame(name=self.cleaned_data["name"], type=self.cleaned_data["type"],
                                    age_range=self.cleaned_data["age_range"])
        if commit:
            instance.save()
        return instance
