import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )

@pytest.mark.django_db
def test_web_login(client, user):
    url = reverse('login')
    data = {'username': 'testuser', 'password': 'testpass123'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('custom_redirect')


@pytest.mark.django_db
def test_password_change(client, user):
    client.login(username='testuser', password='testpass123')
    
    new_password_data = {
        'old_password': 'testpass123',
        'new_password1': 'newtestpassword',
        'new_password2': 'newtestpassword'
    }
    response = client.post(reverse('password_change'), new_password_data)
    assert response.status_code == 302
    assert response.url == reverse('password_change_done')
    
    assert not client.login(username='testuser', password='testpass123')
    assert client.login(username='testuser', password='newtestpassword')

@pytest.mark.django_db
def test_password_reset(client, user):
    response = client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
    assert response.status_code == 302
    assert response.url == reverse('password_reset_done')
    
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Password reset on testserver'

@pytest.mark.django_db
def test_dashboard_view_authenticated(client, user):
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert 'section' in response.context
    assert response.context['section'] == 'dashboard'


@pytest.mark.django_db
def test_dashboard_view_unauthenticated(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302
    assert 'login' in response.url






