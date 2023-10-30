from django.http import HttpResponseNotAllowed
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from profiles.models import Student, Teacher, Manager
from .models import PrivateMessage
from .forms import NewMessageForm
import logging

logger = logging.getLogger(__name__)

class Chat:
    def __init__(self, partner, latest_message, partner_role):
        self.partner = partner
        self.latest_message = latest_message
        self.partner_role = partner_role
        self.partner_id = partner.id

def get_user_profile(user):
    role = None
    profile = None
    if hasattr(user, 'student_profile'):
        profile = user.student_profile
        role = 'student'
    elif hasattr(user, 'teacher_profile'):
        profile = user.teacher_profile
        role = 'teacher'
    elif hasattr(user, 'manager_profile'):
        profile = user.manager_profile
        role = 'manager'
    return profile, role

def get_latest_message(profile, partner):
    try:
        return PrivateMessage.objects.filter(
            Q(sender=partner, receiver=profile.user) | 
            Q(sender=profile.user, receiver=partner)
        ).latest('timestamp')
    except PrivateMessage.DoesNotExist:
        return None

def add_chat(chats, partners, current_profile, user, current_role):
    partner_profile, partner_role = get_user_profile(user)

    if partner_profile.user not in partners:
        partners.add(partner_profile.user)
        try:
            latest_message = PrivateMessage.objects.filter(
                Q(sender=partner_profile.user, receiver=current_profile.user) |
                Q(sender=current_profile.user, receiver=partner_profile.user)
            ).latest('timestamp')
            chats.append(Chat(partner_profile.user, latest_message, partner_role))
        except Exception as e:
            logger.error(f"Error getting latest message for user {user}: {e}")

class MessageListView(ListView):
    model = PrivateMessage
    template_name = 'user_messages/message_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        profile, role = get_user_profile(self.request.user)
        partners = set()
        chats = []
        messages_received = PrivateMessage.objects.filter(receiver=profile.user)
        messages_sent = PrivateMessage.objects.filter(sender=profile.user)

        for msg in messages_received:
            add_chat(chats, partners, profile, msg.sender, role)

        for msg in messages_sent:
            add_chat(chats, partners, profile, msg.receiver, role)

        return chats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = get_user_profile(self.request.user)
        
        if 'chats' in context:
            for chat in context['chats']:
                role_to_model = {
                    'student': Student,
                    'teacher': Teacher,
                    'manager': Manager
                }
                try:
                    partner_user = role_to_model[chat.partner_role].objects.get(id=chat.partner_id).user
                    chat.partner_user = partner_user
                except role_to_model[chat.partner_role].DoesNotExist:
                    logger.error(f"Error retrieving partner with ID {chat.partner_id} and role {chat.partner_role}")
        
        return context

class MessageDetailView(ListView):
    model = PrivateMessage
    template_name = 'user_messages/message_detail.html'
    context_object_name = 'messages'

    def get_queryset(self):
        profile, _ = get_user_profile(self.request.user)
        partner = get_object_or_404(User, pk=self.kwargs['receiver_id'])
        return PrivateMessage.objects.filter(
            Q(sender=profile.user, receiver=partner) | 
            Q(sender=partner, receiver=profile.user)
        ).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner = get_object_or_404(User, pk=self.kwargs['receiver_id'])
        context.update({
            'form': NewMessageForm(),
            'receiver_role': self.kwargs['role'],
            'receiver_id': self.kwargs['receiver_id'],
            'chat': {
                'partner': partner,
                'partner_role': self.kwargs['role']
            }
        })
        return context

    def post(self, request, *args, **kwargs):
        form = NewMessageForm(request.POST)
        if form.is_valid():
            profile, _ = get_user_profile(self.request.user)
            partner = get_object_or_404(User, pk=self.kwargs['receiver_id'])
            message = form.save(commit=False)
            message.sender = profile.user
            message.receiver = partner
            message.save()
            return redirect('message_detail', role=self.kwargs['role'], receiver_id=self.kwargs['receiver_id'])
        return HttpResponseNotAllowed(['POST'])

def send_message(request):
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            profile, _ = get_user_profile(request.user)
            new_message = PrivateMessage(
                content=form.cleaned_data['content'],
                sender=profile.user,
                receiver_id=form.cleaned_data['receiver_id']
            )
            new_message.save()
            return redirect(request.META.get('HTTP_REFERER', '/default/url/'))
    return HttpResponseNotAllowed(['POST'])
