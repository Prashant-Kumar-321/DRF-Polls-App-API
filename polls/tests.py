from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

class PollTest(APITestCase):
    @staticmethod
    def setup_user():
        """Create a API test user"""
        User = get_user_model()

        return User.objects.create_user(
            username='test',
            email='testuser@test.com',
            password='test'
        )

    def setUp(self):
        self.client = APIClient()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.url = '/api/polls/'

    def test_list(self):
        response = self.client.get(
            path=self.url,
            HTTP_AUTHORIZATION = f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200, Received status code {response.status_code} instead"
        )

        self.assertEqual(
            isinstance(response.data, list), 
            True,
            f"Expected response was list, received {type(response.data)} instead"
        )

    def test_create_poll(self):
        data = {
            'question': 'Test Poll'
        }
        
        response = self.client.post(
            path=self.url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            201,
            f'Expected satus code was 201, received {response.status_code} instead'
        )

