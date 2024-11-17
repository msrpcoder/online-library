from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import render
from django.views.generic import TemplateView

from utils.views import BaseLoginView


# Create your views here.
class UserSettingsView(BaseLoginView, TemplateView):
    template_name = "user-settings.html"

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'Settings'
        }

    def post(self, request, **kwargs):
        data = request.POST
        current_password = data.get('current_password', None)
        new_password = data.get('new_password', None)
        new_password_1 = data.get('new_password_1', None)

        errors = {}

        if new_password != new_password_1:
            errors['new_password'] = 'Both new passwords are not same.'

        if not authenticate(username=request.user.username, password=current_password):
            errors['current_password'] = 'Current password is incorrect.'

        if len(errors) > 0:
            return self.get(request, errors=errors)

        self.request.user.set_password(new_password)
        self.request.user.save()
        update_session_auth_hash(request, self.request.user)

        return self.get(request, message='Password changes successfully.')


class UserProfileView(BaseLoginView, TemplateView):
    template_name = "user-profile.html"
