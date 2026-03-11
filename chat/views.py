from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import ChatMessage

User = get_user_model()

@login_required
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id).order_by("username")
    return render(request, "user_list.html", {"users": users})

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related("sender", "receiver")

    # Note: read marking is handled in WebSocket connect for real-time ✓✓ updates.
    return render(request, "chat.html", {
        "other_user": other_user,
        "messages": messages,
    })