from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserAuthenticationTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.test_user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(
            email=self.test_user_data['email'],
            username=self.test_user_data['username'],
            password=self.test_user_data['password']
        )

    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('user-register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        """Test user login endpoint"""
        url = reverse('user-login')
        data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        url = reverse('user-login')
        data = {
            'email': self.test_user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)