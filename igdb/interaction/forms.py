from django import forms
from django.contrib.contenttypes.models import ContentType

from igdb.games.models import VideoGame
from igdb.interaction.models import CuratedList, Review, Like, Comment, Rating

"""
Once again we need to take the user from the kwargs and add him to the form. We pop him from the cleaned data to prevent
tampering and ensure security. We also need to make the user, content_type and object_id fields hidden and not reqiured
so the user doesn't see them. I noticed this code repeating itself several times so I finally made it into a parent 
class.
"""


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


"""
We allow the user to add games by separating their names by a comma. If a game is not found it is skipped. Finally we
save the list once so it creates an id in the database which can then be associated with the list items.
"""


class GenericCuratedListForm(forms.ModelForm):
    items_list = forms.CharField(
        label="Items (comma-separated)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4})
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data.pop("user", None)
        return cleaned_data

    def clean_items_list(self):
        items_list = self.cleaned_data.get("items_list")
        cleaned_items = []

        if items_list:
            items = [item.strip() for item in items_list.split(",")]

            for item in items:
                try:
                    video_game = VideoGame.objects.get(name__iexact=item)
                    cleaned_items.append(video_game)
                except VideoGame.DoesNotExist:
                    pass
        return items_list

    def save(self, commit=True):
        self.clean_items_list()
        curated_list = super().save(commit=False)
        items_list = self.cleaned_data.get("items_list")

        if commit:
            curated_list.save()

        if items_list:
            items = [item.strip() for item in items_list.split(",")]

            for item in items:
                try:
                    video_game = VideoGame.objects.get(name=item)
                    curated_list.items.add(video_game)
                except VideoGame.DoesNotExist:
                    pass
        return curated_list


class CreateCuratedListForm(GenericCuratedListForm):
    class Meta:
        model = CuratedList
        fields = ["title", "description", "user"]

        error_messages = {
            "title": {
                "unique": "A curated list with that name already exists."},
        }

        help_texts = {
            "description": "Enter a short description of the curated list.",
            "items": "Enter a comma-separated list of game names."}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].required = False


class UpdateCuratedListForm(GenericCuratedListForm):
    class Meta:
        model = CuratedList
        fields = ["title", "description"]


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
