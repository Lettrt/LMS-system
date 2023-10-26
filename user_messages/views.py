from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from .models import PrivateMessage

class MessageListView(ListView):
    model = PrivateMessage
    template_name = 'user_messages/message_list.html'

    def get_queryset(self):
        current_user = self.request.user
        
        # Для студентов
        if hasattr(current_user, 'student_profile'):
            current_student = current_user.student_profile
            return PrivateMessage.objects.filter(
                Q(sender_student=current_student) | Q(receiver_student=current_student)
            )
        
        # Для учителей
        elif hasattr(current_user, 'teacher_profile'):
            current_teacher = current_user.teacher_profile
            return PrivateMessage.objects.filter(
                Q(sender_teacher=current_teacher) | Q(receiver_teacher=current_teacher)
            )
        
        # Для менеджеров
        elif hasattr(current_user, 'manager_profile'):
            current_manager = current_user.manager_profile
            return PrivateMessage.objects.filter(
                Q(sender_manager=current_manager) | Q(receiver_manager=current_manager)
            )

        # Если пользователь не подходит под ни одну из категорий, возвращаем пустой запрос
        return PrivateMessage.objects.none()

class MessageDetailView(DetailView):
    model = PrivateMessage
    template_name = 'user_messages/message_detail.html'

    def get_queryset(self):
        current_user = self.request.user
        
        # Для студентов
        if hasattr(current_user, 'student_profile'):
            current_student = current_user.student_profile
            return PrivateMessage.objects.filter(
                Q(sender_student=current_student) | Q(receiver_student=current_student)
            )
        
        # Для учителей
        elif hasattr(current_user, 'teacher_profile'):
            current_teacher = current_user.teacher_profile
            return PrivateMessage.objects.filter(
                Q(sender_teacher=current_teacher) | Q(receiver_teacher=current_teacher)
            )
        
        # Для менеджеров
        elif hasattr(current_user, 'manager_profile'):
            current_manager = current_user.manager_profile
            return PrivateMessage.objects.filter(
                Q(sender_manager=current_manager) | Q(receiver_manager=current_manager)
            )

        # Если пользователь не подходит под ни одну из категорий, возвращаем пустой запрос
        return PrivateMessage.objects.none()
