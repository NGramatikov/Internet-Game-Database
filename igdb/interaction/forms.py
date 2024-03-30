from django import forms
from igdb.interaction.models import CuratedList, Review


class CreateCuratedListForm(forms.ModelForm):
    class Meta:
        model = CuratedList
        fields = ["user", "title",]
