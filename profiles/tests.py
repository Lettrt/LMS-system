from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from profiles.models import Student, Teacher, Manager
from profiles.forms import StudentProfileEditForm

@pytest.mark.django_db
def test_create_student():
    user = User.objects.create_user(username="studentuser", password="testpass")
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    assert student.first_name == "Test"
    assert student.last_name == "Student"
    assert str(student) == "Студент Test Student."

@pytest.mark.django_db
def test_create_teacher():
    user = User.objects.create_user(username="teacheruser", password="testpass")
    teacher = Teacher.objects.create(user=user, first_name="Test", last_name="Teacher")
    assert teacher.first_name == "Test"
    assert teacher.last_name == "Teacher"
    assert str(teacher) == "Ментор Test Teacher."

@pytest.mark.django_db
def test_create_manager():
    user = User.objects.create_user(username="manageruser", password="testpass")
    manager = Manager.objects.create(user=user, first_name="Test", last_name="Manager")
    assert manager.first_name == "Test"
    assert manager.last_name == "Manager"
    assert str(manager) == "Менеджер Test Manager."


@pytest.mark.django_db
def test_valid_student_form():
    user = User.objects.create_user(username="studentuser", password="testpass")
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    data = {
        "email": "test@student.com",
        'date_of_bith': '1989-06-11',
        'phone_number': '+7123981092',
        'bio': 'adsdahsdkljJLSAHffsjdf  fdshfkjh skdfh shdfk hsdkl'
        
    }
    form = StudentProfileEditForm(data, instance=student)
    assert form.is_valid()

@pytest.mark.django_db
def test_invalid_student_form():
    user = User.objects.create_user(username="studentuser", password="testpass")
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    data = {
        "email": "invalidemail", 
        'date_of_bith': '1asd1',
        'phone_number': '+712398sfddsfsdffsdf9991929131932919239311092',
    }
    form = StudentProfileEditForm(data, instance=student)
    assert not form.is_valid()

@pytest.mark.django_db
def test_student_detail_view(client):
    user = User.objects.create_user(username="studentuser", password="testpass")
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    url = reverse('student_detail', kwargs={"pk": student.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["student"] == student

@pytest.mark.django_db
def test_edit_student_profile_by_owner(client):
    user = User.objects.create_user(username="studentuser", password="testpass")
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    client.login(username="studentuser", password="testpass")
    url = reverse('edit_student_profile', kwargs={"pk": student.pk})
    response = client.get(url)
    assert response.status_code == 200

    data = {
        "email": "testchange@student.com",
        'date_of_bith': '1989-06-11',
        'phone_number': '+7123981092',
        'bio': 'adsdahsdkljJLSAHffsjdf  fdshfkjh skdfh shdfk hsdkl'
        
    }
    response = client.post(url, data)
    student.refresh_from_db()
    assert student.email == "testchange@student.com"

@pytest.mark.django_db
def test_edit_student_profile_by_other_user(client):
    user1 = User.objects.create_user(username="studentuser1", password="testpass")
    user2 = User.objects.create_user(username="studentuser2", password="testpass")
    student = Student.objects.create(user=user1, first_name="Test", last_name="Student")
    client.login(username="studentuser2", password="testpass")
    url = reverse('edit_student_profile', kwargs={"pk": student.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('student_detail', kwargs={"pk": student.pk})

@pytest.mark.django_db
def test_redirect_to_student_detail(client):
    user = User.objects.create_user(username="studentuser", password="testpass")
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    client.login(username="studentuser", password="testpass")
    url = reverse('redirect_to_student_detail')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('student_detail', kwargs={"pk": student.pk})

