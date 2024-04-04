from django import forms
from django.contrib.contenttypes.models import ContentType

from igdb.games.models import VideoGame, NonVideoGame
from igdb.interaction.models import CuratedList, Review, Like


class CreateCuratedListForm(forms.ModelForm):
    class Meta:
        model = CuratedList
        fields = ["title", "description", "user", "items"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].required = False

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.pop("user", None)
        return cleaned_data


class UpdateCuratedListForm(forms.ModelForm):
    class Meta:
        model = CuratedList
        fields = ["title", "description", "items"]


class CreateReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        self.content_type = ContentType.objects.get_for_model(VideoGame)
        self.object_id = kwargs.pop("object_id", None)

        super().__init__(*args, **kwargs)

        self.fields["user"].widget = forms.HiddenInput()
        self.fields["content_type"].widget = forms.HiddenInput()
        self.fields["object_id"].widget = forms.HiddenInput()
        self.fields["user"].required = False
        self.fields["content_type"].required = False
        self.fields["object_id"].required = False

    class Meta:
        model = Review
        fields = ["user", "title", "content", "content_type", "object_id"]

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.pop("user", None)
        cleaned_data.pop("content_type", None)
        cleaned_data.pop("object_id", None)
        return cleaned_data


class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "content"]


class CreateLikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ["user", "content_type", "object_id"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        self.content_type = ContentType.objects.get_for_model(VideoGame)
        self.object_id = kwargs.pop("object_id", None)

        super().__init__(*args, **kwargs)

        self.fields["user"].widget = forms.HiddenInput()
        self.fields["content_type"].widget = forms.HiddenInput()
        self.fields["object_id"].widget = forms.HiddenInput()
        self.fields["user"].required = False
        self.fields["content_type"].required = False
        self.fields["object_id"].required = False
