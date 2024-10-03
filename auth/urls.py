from django.urls import path
from .views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("signin", SignInView.as_view(), name="signin"),
    path("logout", SignOutView.as_view(), name="sign-out")
]
