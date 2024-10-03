from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView

from utils.views import BaseLoginView


# Create your views here.
class AdminDashboardView(BaseLoginView, TemplateView):
    template_name = 'admin-dashboard.html'

    def get_login_url(self):
        return reverse('signin')
