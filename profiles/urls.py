from django.urls import path
from . import views

urlpatterns = [
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/edit/<int:pk>/', views.edit_student_profile, name='edit_student_profile'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('redirect_to_student_detail/', views.redirect_to_student_detail, name='redirect_to_student_detail'),
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),

]