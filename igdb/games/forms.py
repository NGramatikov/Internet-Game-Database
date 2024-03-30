from django import forms

from igdb.games.models import VideoGame, NonVideoGame


# We need to check what type of game the user chooses so we can use the appropriate form. This is done via JavaScript in
# the template games\\create
class CreateVideoGameForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        fields = ["name", "age_range", "release_year", "developer", "publisher"]


class CreateNonVideoGameForm(forms.ModelForm):
    class Meta:
        model = NonVideoGame
        fields = ["name", "type", "age_range", "players", "rules", "chance"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["type"] = forms.ChoiceField(choices=(("Party Games", "Party Games"),
                                                         ("Tabletop Games", "Tabletop Games"),
                                                         ("Other Games", "Other Games"),))


class UpdateVideoGameForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        exclude = ["name", "slug", "type"]


class UpdateNonVideoGameForm(forms.ModelForm):
    class Meta:
        model = NonVideoGame
        exclude = ["name", "slug", "type"]
