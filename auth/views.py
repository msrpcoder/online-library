import logging
from logging import getLogger

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from activity.models import Activity
from utils import log_activity
from utils.views import NoCacheMixin

logger = getLogger()


# Create your views here.
class SignUpView(NoCacheMixin, TemplateView):
    template_name = 'signup.html'

    def post(self, request, **kwargs):
        data = request.POST

        username = data.get('username', None)
        password = data.get('password', None)
        email = data.get('email', None)

        errors = {}
        User = get_user_model()
        if not username:
            errors['username'] = 'Enter valid username'
        else:
            try:
                users = User.objects.filter(username=username)
                if len(users) > 0:
                    errors['username'] = 'Select different username'

            except Exception as e:
                logger.exception(e)
                errors['message'] = 'Internal Server Error has occurred.'

        if not password:
            errors['password'] = 'Enter valid password'

        if not email:
            errors['email'] = 'Enter valid email'
        else:
            try:
                users = User.objects.filter(email=email)
                if len(users) > 0:
                    errors['email'] = 'Select different email'

            except Exception as e:
                logger.exception(e)
                errors['message'] = 'Internal Server Error has occurred.'

        if len(errors) > 0:
            return self.get(self.request, errors=errors, user_details=data)

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)

        user.save()

        login(request, user)

        log_activity(user, Activity.Type.USER_SIGNUP, '')

        return redirect('book-catalog')


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
            if request.user.is_superuser:
                return redirect("admin-dashboard")
            else:
                return redirect("book-catalog")
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
                    redirect_url = next_url

                if user.is_superuser:
                    redirect_url = "admin-dashboard"
                else:
                    redirect_url = "book-catalog"

                log_activity(user, Activity.Type.USER_SIGNIN, '')
                return redirect(redirect_url)


class SignOutView(NoCacheMixin, View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            log_activity(request.user, Activity.Type.USER_SIGNOUT, '')
            logout(request)

        return redirect('signin')
