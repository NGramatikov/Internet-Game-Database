from django.urls import path

from igdb.main.views import SignInView, CreateUserView, ReadUserView, UpdateUserView

urlpatterns = [path("sign-in/", SignInView.as_view(), name="sign_in"),
               path("register/", CreateUserView.as_view(), name="create_user"),
               path("users/<int:pk>/", ReadUserView.as_view(), name="read_user"),
               path("users/<int:pk>/update/", UpdateUserView.as_view(), name="update_user")]
