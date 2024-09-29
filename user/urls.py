from django.urls import path

from user.views import UserSettingsView, UserProfileView

urlpatterns = [
    path('settings', UserSettingsView.as_view(), name='user-settings'),
    path('profile', UserProfileView.as_view(), name='user-profile')
]