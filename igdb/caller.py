import os
from datetime import datetime

import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "igdb.settings")
django.setup()

from igdb.main.models import Profile
from django.contrib.auth.models import User
from igdb.games.models import VideoGame, NonVideoGame, Game
from django.contrib.contenttypes.models import ContentType
from igdb.interaction.models import CuratedList, Like, Comment, Review, Rating, GenericInteraction, Likeable, Rateable, \
    Commentable, Reviewable


'''
Preventing SQL injection:
    Django's ORM abstracts away direct SQL queries and automatically escapes user input, significantly reducing 
    the risk of SQL injection.

Preventing XSS:
    Django's template engine comes with built-in protections against XSS. Namely in settings.py> middleware:
        'django.middleware.security.SecurityMiddleware'

Preventing CSRF:
    Django provides CSRF protection by generating and validating unique tokens for each user session. Also in 
    settings.py> middleware> 'django.middleware.csrf.CsrfViewMiddleware' and in every form: {% csrf_token %}

Preventing parameter tampering:
    We use the @login_required decorator for function-based views and the LoginRequiredMixin for class-based views.
    Also we have added checks on all of the Update views that the user accessing them is the same user who created them.
'''

# def_user = User(username="user1", password="pass1")
# def_user.save()
# cust_user = Profile(user=def_user, description="This is the first profile")
# cust_user.save()
# video_game1 = VideoGame(name="Video Game 1", type="Video Games", age_range=12)
# video_game1.save()
# non_video_game1 = NonVideoGame(name="Non-video Game 1", type="Party Games", age_range=16, players=4, rules="game rules1")
# non_video_game1.save()
# curated_list1 = CuratedList(author=user.user)
# curated_list1.save()

user = Profile.objects.all().first()
video_game1 = VideoGame.objects.all().first()
non_video_game1 = NonVideoGame.objects.all().first()
curated_list1 = CuratedList.objects.all().first()

''' To add items to curated list we need to get their content type and object id like this: '''
# list_item1 = ListItem(curated_list=curated_list1, content_type=ContentType.objects.get_for_model(VideoGame),
#                       object_id=video_game1.id)
# list_item1.save()
# list_item2 = ListItem(curated_list=curated_list1, content_type=ContentType.objects.get_for_model(NonVideoGame),
#                       object_id=non_video_game1.id)
# list_item2.save()

''' Accessing the list of games in a CuratedList.'''
# curated_list1_items = ListItem.objects.filter(curated_list=curated_list1)

''' If we want to access the original object: '''
# curated_list_item = curated_list1_items.get(id=1).content_object

''' To create a Like once again we need to get the content type and object id of the object we want to like: '''
# like = Like(user=user.user, content_type=ContentType.objects.get_for_model(VideoGame), object_id=video_game1.id)
# like.save()
# like = Like.objects.all().first()
''' After that we can access both the liked object through the like and vice versa: '''
# game_object1 = like.content_object
# like_object = video_game1.likes.get(id=like.id)

''' Hopefully the same goes for the Rate, Comment and Review classes... '''
# rating = Rating(user=user.user, content_type=ContentType.objects.get_for_model(VideoGame), object_id=video_game1.id,
#                 rating=10)
# rating.save()
# rating = Rating.objects.all().first()
# game_object2 = rating.content_object
# rating_object = video_game1.ratings.get(id=rating.id)

# comment = Comment(user=user.user, content_type=ContentType.objects.get_for_model(NonVideoGame),
#                   object_id=non_video_game1.id, comment="This is a comment")
# comment.save()
# comment = Comment.objects.all().first()
# game_object3 = comment.content_object
# comment_object = non_video_game1.comments.get(id=comment.id)

# review = Review(user=user.user, content_type=ContentType.objects.get_for_model(VideoGame), object_id=video_game1.id,
#                 review="This is a review")
# review.save()
# review = Review.objects.all().first()
# game_object4 = review.content_object
# review_object = video_game1.reviews.get(id=review.id)

''' And now, just because, let's try to like and comment on a CuratedList: '''
# like2 = Like(user=user.user, content_type=ContentType.objects.get_for_model(CuratedList), object_id=curated_list1.id)
# like2.save()
# comment2 = Comment(user=user.user, content_type=ContentType.objects.get_for_model(CuratedList),
#                    object_id=curated_list1.id)
# comment2.save()
# print(curated_list1.likes.all())
# print(curated_list1.comments.all())

''' 
To summarize: object1.interaction1 returns GenericRelatedManager, while object1.interaction1.all() returns a QuerySet.
From there we can always use object1.interactions.get(id=inter_obj.id) to get an instance of the interaction object.
Or, if we are so inclined, we can use inter_obj.content_object to get the original object.
'''

'''
TODO: Make sure a user can't like an object more than once.
'''

# game3 = VideoGame(name="Max Payne 2: The Fall of Max Payne", type="Video Games", age_range=18, release_year=2003,
#                   developer="Remedy", publisher="Rockstar")
# game3.save()
# game3 = VideoGame.objects.get(name="Max Payne 2: The Fall of Max Payne")
# print(game3.__str__())
# game4 = VideoGame(name="CoD2", type="Video Games", age_range=16, release_year=2005, developer="Activision",
#                   publisher="Activision")
# game4.save()
# user2 = User.objects.get(id="7")
# profile2 = Profile(user=user2, birthdate="2011-03-27")
# profile2.save()
# print(VideoGame.objects.first().reviews.all())
# ContentType.objects.get_for_model

content_types = []
all_models = [Game, VideoGame, NonVideoGame, GenericInteraction, Like, Likeable, Rating, Rateable, Comment, Commentable,
              Review, Reviewable, CuratedList]

inter_models = [VideoGame, NonVideoGame]
for model in inter_models:
    content_types.append(ContentType.objects.get_for_model(model))
# print(content_types)

# comment = Comment.objects.get(id=1)
# print(comment.content_object.slug)

game1 = VideoGame.objects.get(slug="call-of-du-3")
user1 = User.objects.get(id=1)
for like in game1.likes.all():
    if like.user == user1:
        print("Yes")

rating = Rating.objects.all().filter(user=User.objects.get(id=1)).first()
print(rating.content)
