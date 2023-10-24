from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

class WebAuthTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
    
    def test_web_login(self):
        """Тестирование входа в систему через веб-интерфейс"""
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        
        # проверка перенаправления
        self.assertRedirects(response, reverse('dashboard'))

    def test_password_change(self):
        # авторизация перед сменой пароля
        self.client.login(username='testuser', password='testpass123')
        
        new_password_data = {
            'old_password': 'testpass123',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword'
        }
        response = self.client.post(reverse('password_change'), new_password_data)
        self.assertRedirects(response, reverse('password_change_done'))
        
        # проверка нового пароля (старый не работает, новый работает)
        self.assertFalse(self.client.login(username='testuser', password='testpass123'))
        self.assertTrue(self.client.login(username='testuser', password='newtestpassword'))

    def test_password_reset(self):
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
        
        # проверка отправки письма
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')
