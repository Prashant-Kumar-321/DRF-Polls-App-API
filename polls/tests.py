from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token

from .views import PollViewSets

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
        self.factory = APIRequestFactory()
        self.view = PollViewSets.as_view({'post' : 'list'})

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

        print(response.data)

        self.assertEqual(
            response.status_code,
            201,
            f'Expected satus code was 201, received {response.status_code} instead'
        )

    def test_create_a_poll_without_authentication_token(self):
        data = {
            'question': 'Test Poll'
        }

        request = self.factory.post(
            path=self.url,
            data=data,
        )

        response = self.view(request)

        self.assertEqual(
            response.status_code,
            401,
            f"Expected status code was 401, Received {response.status_code} instead"
        )
    
    def test_create_a_poll_without_authentication_token2(self): 
        data={
            'question': 'Test Poll'
        }

        response = self.client.post(
            path=self.url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            401,
            f'Expected status code 401(UnAuthorized access), recevied {response.status_code} instead'
        )

    def test_retreive_a_poll(self):
        """Test retrieving a specific poll"""

        # Create a poll
        poll_data={'question': 'How are you?'}
        create_response = self.client.post(
            path=self.url,
            data=poll_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        poll_id = create_response.data['id']

        # Retreive the poll
        response = self.client.get(
            path=f'{self.url}{poll_id}/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data['question'],
            poll_data['question']
        )

    def test_update_poll(self):
        """Test updating an existing poll"""

        # Create a poll
        poll_data={'question': 'Original Question'}
        create_response = self.client.post(
            path=self.url,
            data=poll_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        poll_id=create_response.data['id']

        # Update the poll
        update_data={'question': 'Updated Question'}
        response = self.client.put(
            path=f'{self.url}{poll_id}/',
            data=update_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data['question'],
            update_data['question']
        )
