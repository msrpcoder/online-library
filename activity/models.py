from django.contrib.auth import get_user_model
from django.db.models import Model, ForeignKey, DateTimeField, TextField, CASCADE

User = get_user_model()


# Create your models here.
class Activity(Model):
    actor = ForeignKey(User, on_delete=CASCADE)
    timestamp = DateTimeField(auto_now_add=True)
    activity_type = TextField(null=False, blank=False)
    object_details = TextField(null=True)
    description = TextField(null=False, blank=False)

    class Type(object):
        USER_SIGNUP = "User signup"
        USER_SIGNIN = "User login"
        USER_SIGNOUT = "User logout"
        BOOK_ADDED = "Book Added"
        BOOK_PREVIEWED = "Book read"
