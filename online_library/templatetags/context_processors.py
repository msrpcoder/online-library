import os

from django import template
from django.conf import settings

register = template.Library()


def profile_image_exists(request):
    if not request.user:
        return {
            profile_image_exists: False
        }

    return {
        'profile_image_exists': os.path.exists(os.path.join(settings.MEDIA_ROOT, str(request.user.id), 'profile.png'))
    }
