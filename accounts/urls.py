from django.urls import path
from .views import register_view, EmailLoginView, UserLogoutView

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]