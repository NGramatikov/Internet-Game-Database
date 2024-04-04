from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.defaultfilters import slugify

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
    title = models.CharField(max_length=100, null=False, blank=False, unique=True, validators=[MinLengthValidator(10)])
    content = models.TextField(null=False, blank=False, validators=[MinLengthValidator(20)])
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.title[:10]}-{self.pk}")
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Review {self.title} was created by {self.user.username} on {self.created_at}"


class Reviewable(models.Model):
    class Meta:
        abstract = True
    reviews = GenericRelation(Review)


class CuratedList(models.Model):
    user = models.ForeignKey(to=user, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, null=False, blank=False, unique=True, validators=[validate_title])
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(to="games.VideoGame")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.title[:10]}-{self.pk}")
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} list was created by {self.user.username}"


# class ListItem(models.Model):
#     curated_list = models.ForeignKey(CuratedList, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     def __str__(self):
#         return f'{self.curated_list.title} - {self.content_object}'
