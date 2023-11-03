import pytest
from django.test import RequestFactory, TestCase
from unittest.mock import patch
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from lesson.models import Lesson, Progress
from user_messages.forms import NewMessageForm
from user_messages.models import PrivateMessage
from .models import Student, Teacher, Manager
from .forms import StudentProfileEditForm, TeacherProfileEditForm
from profiles.models import Student
from profiles.forms import StudentProfileEditForm
from profiles.views import UserMixin, StudentDetailView

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestUserMixin:
    
    def test_get_partner_role_student(self):
        user = mixer.blend(User)
        mixer.blend('profiles.Student', user=user)
        assert UserMixin.get_partner_role(user) == 'student', "Should return 'student' for users with a student profile"

    def test_get_partner_role_teacher(self):
        user = mixer.blend(User)
        mixer.blend('profiles.Teacher', user=user)
        assert UserMixin.get_partner_role(user) == 'teacher', "Should return 'teacher' for users with a teacher profile"

    def test_get_partner_role_manager(self):
        user = mixer.blend(User)
        mixer.blend('profiles.Manager', user=user)
        assert UserMixin.get_partner_role(user) == 'manager', "Should return 'manager' for users with a manager profile"

    def test_get_partner_role_none(self):
        user = mixer.blend(User)
        assert UserMixin.get_partner_role(user) is None, "Should return None for users with no specific profile"

def test_student_creation():
    user = mixer.blend(User)
    student = mixer.blend(Student, user=user)
    assert student.__str__() == f'Студент {student.first_name} {student.last_name}.', 'Should create a Student'

def test_teacher_creation():
    user = mixer.blend(User)
    teacher = mixer.blend(Teacher, user=user)
    assert teacher.__str__() == f'Ментор {teacher.first_name} {teacher.last_name}.', 'Should create a Teacher'

def test_manager_creation():
    user = mixer.blend(User)
    manager = mixer.blend(Manager, user=user)
    assert manager.__str__() == f'Менеджер {manager.first_name} {manager.last_name}.', 'Should create a Manager'

def test_student_form_valid():
    form_data = {'email': 'test@example.com', 'date_of_bith': '1990-01-01'}
    form = StudentProfileEditForm(data=form_data)
    assert form.is_valid(), 'Should be valid if the fields are correct'

def test_teacher_form_valid():
    form_data = {'email': 'test@example.com', 'date_of_bith': '1980-01-01'}
    form = TeacherProfileEditForm(data=form_data)
    assert form.is_valid(), 'Should be valid if the fields are correct'

def test_student_list_view(client, django_user_model):
    url = reverse('student_list')
    response = client.get(url)
    assert response.status_code == 200, 'Should be callable by anyone'

def test_teacher_list_view(client, django_user_model):
    url = reverse('teacher_list')
    response = client.get(url)
    assert response.status_code == 200, 'Should be callable by anyone'

@pytest.fixture
def user_with_profile(db, request):
    user = mixer.blend('auth.User')
    mixer.blend(f'profiles.{request.param}', user=user)
    return user

@pytest.fixture
def message_data():
    return {'content': 'Test message content'}

@pytest.mark.django_db
@pytest.mark.parametrize('user_with_profile', ['Student', 'Teacher', 'Manager'], indirect=True)
def test_send_message_valid(user_with_profile, message_data):
    request = HttpRequest()
    request.user = user_with_profile
    request.POST = message_data
    receiver = mixer.blend('auth.User')
    success, form = UserMixin.send_message(request, receiver)
    assert success is True
    assert PrivateMessage.objects.last().sender == request.user
    assert PrivateMessage.objects.last().receiver == receiver

@pytest.mark.django_db
@pytest.mark.parametrize('user_with_profile', ['Student', 'Teacher', 'Manager'], indirect=True)
def test_send_message_invalid_form(user_with_profile):
    request = HttpRequest()
    request.user = user_with_profile
    request.POST = {}
    receiver = mixer.blend('auth.User')
    success, form = UserMixin.send_message(request, receiver)
    assert success is False
    assert not form.is_valid()

@pytest.fixture
def student(db):
    return mixer.blend('profiles.Student')

@pytest.fixture
def user(db):
    return mixer.blend('auth.User')

@pytest.mark.django_db
def test_student_detail_view_context_data(student, user):
    request = RequestFactory().get('/fake-path')
    request.user = user
    view = StudentDetailView()
    view.object = student
    view.request = request
    context = view.get_context_data()

    assert 'form' in context
    assert isinstance(context['form'], StudentProfileEditForm)
    assert context['form'].instance == student, "Form instance should be the student"

    assert 'message_form' in context
    assert isinstance(context['message_form'], NewMessageForm)

    assert 'partner_id' in context
    assert context['partner_id'] == student.user_id, "Partner ID should match student's user ID"

@pytest.fixture
def student_user(db):
    return mixer.blend(User)

@pytest.fixture
def student(db, student_user):
    return mixer.blend(Student, user=student_user)

@pytest.mark.django_db
def test_get_progress_percentage(student):
    request = RequestFactory().get('/fake-path')
    request.user = student.user

    with patch('profiles.views.StudentDetailView.get_total_lessons_count', return_value=15), \
         patch('profiles.views.StudentDetailView.get_completed_lessons_count', return_value=9):
        view = StudentDetailView()
        view.object = student
        view.request = request
        progress_percentage = view.get_progress_percentage()
        expected_percentage = (9 / 15) * 100
        assert progress_percentage == expected_percentage, "Progress percentage should be correctly calculated"

        context = view.get_context_data()
        assert 'progress_percentage' in context
        assert context['progress_percentage'] == expected_percentage, "Progress percentage should be correctly calculated and included in context"

@pytest.fixture
def user(db):
    return mixer.blend('auth.User')

@pytest.fixture
def student(db, user):
    return mixer.blend('profiles.Student', user=user)

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.mark.django_db
class TestStudentDetailView2:

    @patch('profiles.views.StudentDetailView.get_object')
    @patch('profiles.views.StudentDetailView.send_message')
    def test_post_message_sent(self, mock_send_message, mock_get_object, request_factory, student):
        mock_send_message.return_value = (True, None)
        mock_get_object.return_value = student
        request = request_factory.post('/fake-path')
        request.user = student.user
        response = StudentDetailView.as_view()(request, pk=student.pk)
        assert response.status_code == 302
        assert response.url == f'/profiles/student/{student.pk}/'

    @patch('profiles.views.StudentDetailView.get_object')
    @patch('profiles.views.StudentDetailView.send_message')
    def test_post_message_not_sent(self, mock_send_message, mock_get_object, request_factory, student):
        mock_send_message.return_value = (False, 'message_form')
        mock_get_object.return_value = student
        request = request_factory.post('/fake-path')
        request.user = student.user
        response = StudentDetailView.as_view()(request, pk=student.pk)

        assert response.status_code == 200
        assert 'message_form' in response.context_data