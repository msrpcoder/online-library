from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View


class NoCacheMixin(View):
    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        #resp['pragma'] = 'no-cache'
        resp['cache-control'] = 'no-store'
        #resp['expires'] = 0

        return resp


class BaseLoginView(NoCacheMixin, LoginRequiredMixin, View):
    def get_login_url(self):
        return reverse('signin')
