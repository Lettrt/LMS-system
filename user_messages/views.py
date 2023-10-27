from django.http import HttpResponseNotAllowed
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from profiles.models import Student, Teacher, Manager
from .models import PrivateMessage
from .forms import NewMessageForm

class Chat:
    def __init__(self, partner, latest_message, partner_role):
        self.partner = partner
        self.latest_message = latest_message
        self.partner_role = partner_role
        self.partner_id = partner.id

def get_user_profile(user):
    role = None
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

class MessageListView(ListView):
    model = PrivateMessage
    template_name = 'user_messages/message_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        current_profile, role = get_user_profile(self.request.user)

        partners = set()
        chats = []

        messages_received = PrivateMessage.objects.filter(receiver=current_profile.user)
        messages_sent = PrivateMessage.objects.filter(sender=current_profile.user)

        for msg in messages_received:
            if msg.sender not in partners:
                partners.add(msg.sender)
                latest_message = PrivateMessage.objects.filter(
                    Q(sender=msg.sender, receiver=current_profile.user) | 
                    Q(sender=current_profile.user, receiver=msg.sender)
                ).latest('timestamp')
                chats.append(Chat(msg.sender, latest_message, role))

        for msg in messages_sent:
            if msg.receiver not in partners:
                partners.add(msg.receiver)
                latest_message = PrivateMessage.objects.filter(
                    Q(sender=msg.receiver, receiver=current_profile.user) | 
                    Q(sender=current_profile.user, receiver=msg.receiver)
                ).latest('-timestamp')
                chats.append(Chat(msg.receiver, latest_message, role))

        return chats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context['chats']:
            for chat in context['chats']:
                partner_id = chat.partner_id
                partner_role = chat.partner_role
                print(f"Partner ID: {partner_id}, Partner Role: {partner_role}")  # Debug output
                partner = None
                student = self.request.user.student_profile
                context['student'] = student
                if partner_role == 'student':
                    partner = Student.objects.get(id=partner_id).user
                elif partner_role == 'teacher':
                    partner = Teacher.objects.get(id=partner_id).user
                elif partner_role == 'manager':
                    partner = Manager.objects.get(id=partner_id).user

                chat.partner_user = partner 

        return context

class MessageDetailView(ListView):
    model = PrivateMessage
    template_name = 'user_messages/message_detail.html'
    context_object_name = 'messages'

    def get_queryset(self):
        current_profile, role = get_user_profile(self.request.user)
        receiver_role = self.kwargs['role']
        partner_id = self.kwargs['receiver_id']
        partner = get_object_or_404(User, pk=partner_id)

        return PrivateMessage.objects.filter(
            Q(sender=current_profile.user, receiver=partner) | 
            Q(sender=partner, receiver=current_profile.user)
        ).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_profile, _ = get_user_profile(self.request.user)
        receiver_role = self.kwargs['role']
        partner_id = self.kwargs['receiver_id']
        partner = get_object_or_404(User, pk=partner_id)

        context['form'] = NewMessageForm()
        context['receiver_role'] = receiver_role
        context['receiver_id'] = partner_id
        context['chat'] = {
            'partner': partner,
            'partner_role': receiver_role
        }

        return context
    
    def post(self, request, *args, **kwargs):
        form = NewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            current_profile, _ = get_user_profile(self.request.user)
            receiver_role = self.kwargs['role']
            partner_id = self.kwargs['receiver_id']
            partner = get_object_or_404(User, pk=partner_id)
            
            message.sender = current_profile.user
            message.receiver = partner
            message.save()
            
        return redirect('message_detail', role=receiver_role, receiver_id=partner_id)


def send_message(request):
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            receiver_id = form.cleaned_data['receiver_id']
            message_content = form.cleaned_data['content']

            current_profile, role = get_user_profile(request.user)

            new_message = PrivateMessage(
                content=message_content,
                sender=current_profile.user,
                receiver_id=receiver_id
            )
            new_message.save()

            return redirect(request.META.get('HTTP_REFERER', '/default/url/'))
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        return HttpResponseNotAllowed(['POST'])
