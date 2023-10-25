from django.views.generic import ListView, DetailView
from .models import Course, Rating

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            course.top_comments = course.comments.all()[:3]
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"
