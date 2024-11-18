from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse
from django.views.generic import TemplateView

from activity.models import Activity
from books.models import Book
from utils.views import BaseLoginView


# Create your views here.
class AdminDashboardView(BaseLoginView, TemplateView):
    template_name = 'admin-dashboard.html'

    def get_login_url(self):
        return reverse('signin')

    def get_context_data(self, **kwargs):
        total_activity = Activity.objects.filter(activity_type='Book read').values('object_details').annotate(total=Count('object_details')).order_by('-total')
        top_10_books_activity = total_activity[:10]
        books_map = {}
        books = Book.objects.filter(isbn_no__in=map(lambda x: x['object_details'], top_10_books_activity))

        for book in books:
            books_map[book.pk] = book

        for activity in top_10_books_activity:
            activity['book'] = books_map[activity['object_details']]

        top_books_by_genre = Book.objects.filter(isbn_no__in=map(lambda x: x['object_details'], total_activity)).values('genre').annotate(total=Count('genre')).order_by('-total')

        return {
            **kwargs,
            'page_header': 'Dashboard',
            'activities': Activity.objects.all().order_by('-timestamp')[:10],
            'total_books': Book.objects.count(),
            'total_users': get_user_model().objects.count(),
            'top_10_books': top_10_books_activity,
            'top_by_genre': top_books_by_genre
        }
