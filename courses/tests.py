import pytest
from django.contrib.auth.models import User
from .models import Course, Comment, Rating, CourseApplication
from profiles.models import Student

@pytest.mark.django_db
def test_course_creation():
    course = Course.objects.create(
        title="Course 1",
        descritption="Sample course description",
        duration="1 week"
    )
    assert Course.objects.count() == 1
    assert course.average_rating == "Ещё нет рейтинга"

@pytest.mark.django_db
def test_comment_creation():
    course = Course.objects.create(
        title="Course 1",
        descritption="Sample course description",
        duration="1 week"
    )
    user = User.objects.create_user(username='testuser', password='password')
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    comment = Comment.objects.create(
        course=course,
        student=student,
        text="Sample comment text"
    )
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_rating_creation():
    course = Course.objects.create(
        title="Course 1",
        descritption="Sample course description",
        duration="1 week"
    )
    user = User.objects.create_user(username='testuser', password='password')
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")
    rating = Rating.objects.create(
        course=course,
        student=student,
        rating=3
    )
    assert Rating.objects.count() == 1

@pytest.mark.django_db
def test_course_application_creation():
    application = CourseApplication.objects.create(
        name="Test User",
        email="testuser@example.com",
        phone_number="+1234567890",
        message="Sample application message"
    )
    assert CourseApplication.objects.count() == 1

@pytest.mark.django_db
def test_average_rating():
    course = Course.objects.create(
        title="Test Course",
        descritption="Test Description",
        duration="1 week"
    )
    user1 = User.objects.create_user(username='testuser1', password='password')
    student1 = Student.objects.create(user=user1, first_name="Test1", last_name="Student1")
    
    user2 = User.objects.create_user(username='testuser2', password='password')
    student2 = Student.objects.create(user=user2, first_name="Test2", last_name="Student2")

    assert course.average_rating == 'Ещё нет рейтинга'
    Rating.objects.create(course=course, student=student1, rating=4)
    Rating.objects.create(course=course, student=student2, rating=2)
    assert course.average_rating == 3


@pytest.mark.django_db
def test_rating_uniqueness():
    course = Course.objects.create(
        title="Test Course",
        descritption="Test Description",
        duration="1 week"
    )
    user = User.objects.create_user(username='testuser', password='password')
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")

    Rating.objects.create(course=course, student=student, rating=4)

    with pytest.raises(Exception):
        Rating.objects.create(course=course, student=student, rating=3)

@pytest.mark.django_db
def test_model_relationships():
    course = Course.objects.create(
        title="Test Course",
        descritption="Test Description",
        duration="1 week"
    )
    user = User.objects.create_user(username='testuser', password='password')
    student = Student.objects.create(user=user, first_name="Test", last_name="Student")

    comment = Comment.objects.create(course=course, student=student, text="Test comment")
    assert Comment.objects.count() == 1

    course.delete()
    assert Comment.objects.count() == 0
