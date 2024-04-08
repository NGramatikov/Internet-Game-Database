from django import forms
from django.contrib.contenttypes.models import ContentType

from igdb.games.models import VideoGame
from igdb.interaction.models import CuratedList, Review, Like, Comment, Rating

'''
Once again we need to take the user from the kwargs and add him to the form. We pop him from the cleaned data to prevent
tampering and ensure security. We also need to make the user, content_type and object_id fields hidden and not reqiured
so the user doesn't see them. I noticed this code repeating itself several times so I finally made it into a parent 
class.
'''


class CreateGenericInteractionForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.pop("user", None)
        cleaned_data.pop("content_type", None)
        cleaned_data.pop("object_id", None)
        return cleaned_data


class CreateCuratedListForm(forms.ModelForm):
    class Meta:
        model = CuratedList
        fields = ["title", "description", "user", "items"]

        error_messages = {
            "title": {
                "unique": "A curated list with that name already exists."},
        }

        help_texts = {
            "description": "Enter a short description of the curated list.",
            "items": "Enter a comma-separated list of items."}

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


class CreateReviewForm(CreateGenericInteractionForm):
    class Meta:
        model = Review
        fields = ["user", "title", "content", "content_type", "object_id"]
        error_messages = {"title": {"unique": "A review with that name already exists."}}


class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "content"]


class CreateLikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []


class DeleteLikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []


class CreateCommentForm(CreateGenericInteractionForm):
    class Meta:
        model = Comment
        fields = ["user", "content", "content_type", "object_id"]


class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CreateRatingForm(CreateGenericInteractionForm):
    class Meta:
        model = Rating
        fields = ["user", "content", "content_type", "object_id"]


class UpdateRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["content"]
