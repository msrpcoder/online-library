from django.shortcuts import render
from django.views.generic import TemplateView

from utils.views import BaseLoginView


# Create your views here.
class UserSettingsView(BaseLoginView, TemplateView):
    template_name = "user-settings.html"


class UserProfileView(BaseLoginView, TemplateView):
    template_name = "user-profile.html"
