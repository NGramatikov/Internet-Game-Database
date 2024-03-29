from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from igdb.interaction.validators import validate_title

# Create your models here.
user = get_user_model()
RATINGS = [(i, i) for i in range(1, 11)]


class GenericInteraction(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(to=user, on_delete=models.DO_NOTHING)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)


class Like(GenericInteraction):
    pass


class Likeable(models.Model):
    class Meta:
        abstract = True
    likes = GenericRelation(Like)


class Rating(GenericInteraction):
    content = models.PositiveSmallIntegerField(choices=RATINGS)


class Rateable(models.Model):
    class Meta:
        abstract = True
    ratings = GenericRelation(Rating)


class Comment(GenericInteraction):
    content = models.TextField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)


class Commentable(models.Model):
    class Meta:
        abstract = True
    comments = GenericRelation(Comment)


class Review(GenericInteraction):
    content = models.TextField(null=False, blank=False, validators=[MinLengthValidator(20)])
    updated_at = models.DateTimeField(auto_now=True)


class Reviewable(models.Model):
    class Meta:
        abstract = True
    reviews = GenericRelation(Review)


# If we try to change the order of inheritance we will get a circular import error when migrating
class CuratedList(Likeable, Commentable, models.Model):
    user = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, null=False, blank=False, unique=True, validators=[validate_title])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ListItem(models.Model):
    curated_list = models.ForeignKey(CuratedList, on_delete=models.DO_NOTHING)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.curated_list.title} - {self.content_object}'
