from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from utils.views import NoCacheMixin


# Create your views here.
class SignUpView(NoCacheMixin, TemplateView):
    template_name = 'signup.html'


class SignInView(NoCacheMixin, TemplateView):
    template_name = 'signin.html'

    def get_context_data(self, **kwargs):
        out = super().get_context_data(**kwargs)
        next = self.request.GET.get('next')

        if next:
            out['next'] = next

        return out

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("admin-dashboard")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

            if not username and not password:
                return self.get(request, errors={'username': 'Invalid Username', 'password': 'Invalid Password'})

            elif not username:
                return self.get(request, errors={'username': 'Invalid Username'})

            elif not password:
                return self.get(request, errors={'password': 'Invalid Password'})

            user = authenticate(username=username, password=password)
            if not user:
                return self.get(request, errors={'general': 'Invalid username/password'})
            else:
                login(request, user)
                next_url = request.POST.get("next")
                if next_url:
                    return redirect(next_url)

                return redirect("admin-dashboard")


class SignOutView(NoCacheMixin, View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)

        return redirect('signin')
