from django.views.generic import ListView, DetailView

from courses.models import Course
from .models import Library

class LibraryListViiew(ListView):
    model = Library
    template_name = 'library/library_list.html'
    context_object_name = 'library_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        course_id = self.request.GET.get('course')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context
    
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library/library_detail.html'
    context_object_name = 'library_detail'