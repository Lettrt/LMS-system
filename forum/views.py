from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Prefetch
from .models import Topic, Subtopic, Post
from .forms import PostForm

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'forum/topic_list.html'
    paginate_by = 10

class SubtopicListView(ListView):
    model = Subtopic
    context_object_name = 'subtopics'
    template_name = 'forum/subtopic_list.html'
    paginate_by = 10

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        queryset = Subtopic.objects.filter(topic_id=topic_id)
        return queryset

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        last_posts_prefetch = Prefetch(
            'posts', 
            queryset=Post.objects.select_related(
                'created_by__student_profile',
                'created_by__teacher_profile',
                'created_by__manager_profile'
            ).order_by('-created_at')[:5],
            to_attr='last_posts'
        )
        queryset = Subtopic.objects.filter(topic_id=topic_id).prefetch_related(last_posts_prefetch)
        return queryset
    
class SubtopicDetailView(DetailView):
    model = Subtopic
    context_object_name = 'subtopic'
    template_name = 'forum/subtopic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subtopic = context['subtopic']
        posts_with_profiles = subtopic.posts.order_by('-created_at').select_related(
            'created_by__student_profile', 
            'created_by__teacher_profile', 
            'created_by__manager_profile'
        )

        for post in posts_with_profiles:
            user = post.created_by
            post.profile = getattr(user, 'student_profile', 
                                   getattr(user, 'teacher_profile', 
                                           getattr(user, 'manager_profile', None)))

        context['posts_with_profiles'] = posts_with_profiles
        context['post_form'] = PostForm()
        return context
    
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.subtopic_id = self.kwargs['subtopic_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('subtopic_detail', kwargs={'pk': self.kwargs['subtopic_id']})