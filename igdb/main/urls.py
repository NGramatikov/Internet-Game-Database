from django.urls import path

from igdb.main.views import SignOutView, CreateUserView, ReadUserView, UpdateUserView, sign_in

urlpatterns = [path("sign-in/", sign_in, name="sign_in"),
               path("sign-out", SignOutView.as_view(), name="sign_out"),
               path("register/", CreateUserView.as_view(), name="create_user"),
               path("users/<int:pk>/", ReadUserView.as_view(), name="read_user"),
               path("users/<int:pk>/update/", UpdateUserView.as_view(), name="update_user")]
