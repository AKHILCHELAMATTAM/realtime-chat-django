# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib.auth.views import LoginView, LogoutView
# from .forms import RegisterForm
# from .forms import RegisterForm

# def register_view(request):
#     if request.user.is_authenticated:
#         return redirect("user_list")

#     form = RegisterForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         user = form.save()
#         login(request, user)
#         return redirect("user_list")

#     return render(request, "register.html", {"form": form})

# class EmailLoginView(LoginView):
#     template_name = "login.html"

# class UserLogoutView(LogoutView):
#     pass

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, BootstrapAuthForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("user_list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("user_list")

    return render(request, "register.html", {"form": form})

class EmailLoginView(LoginView):
    template_name = "login.html"
    authentication_form = BootstrapAuthForm

class UserLogoutView(LogoutView):
    pass