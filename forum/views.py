from django.views.generic import ListView, DetailView, CreateView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for subtopic in context['subtopics']:
            subtopic.last_posts = subtopic.posts.order_by('-created_at')[:5]
        return context
    
class SubtopicDetailView(DetailView):
    model = Subtopic
    context_object_name = 'subtopic'
    template_name = 'forum/subtopic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subtopic = context['subtopic']
        context['last_posts'] = subtopic.posts.order_by('-created_at')[:5]
        return context
    
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/create_post.html'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.subtopic_id = self.kwargs['subtopic_id']
        return super().form_valid(form)