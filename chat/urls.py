from django.urls import path
from .views import user_list_view, chat_view

urlpatterns = [
    path("", user_list_view, name="user_list"),
    path("chat/<int:user_id>/", chat_view, name="chat"),
]