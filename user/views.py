import os
import logging

from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.generic import TemplateView

from online_library import settings
from utils.views import BaseLoginView

logger = logging.getLogger()


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

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'User-Profile',
            'user_id': self.request.user.id,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email
        }

    def post(self, request, **kwargs):
        data = request.POST
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)

        errors = {}
        if not first_name:
            errors['first_name'] = 'Enter first-name'

        if not last_name:
            errors['last_name'] = 'Enter last-name'

        if not email:
            errors['email'] = 'Enter email'

        if len(errors) > 0:
            return self.get(request, errors=errors)

        user = self.request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        profile_image_file = request.FILES.get('profile_image', None)
        if profile_image_file:
            user_profile_path = os.path.join(settings.MEDIA_ROOT, str(user.id))

            try:
                os.makedirs(user_profile_path)
            except FileExistsError:
                logger.error(f"Folder already exists {user_profile_path}")

            image_path = os.path.join(user_profile_path, 'profile.png')
            with open(image_path, 'wb') as fp:
                for chunk in profile_image_file.chunks():
                    fp.write(chunk)

        return self.get(request, message='Profile updated successfully.')