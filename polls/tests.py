from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token

import uuid

from .views import PollViewSets

class PollTest(APITestCase):
    @staticmethod
    def get_user(user_credentials=None):
        """Create a API test user"""
        User = get_user_model()

        if not user_credentials: 
            return User.objects.create_user(
                username='test',
                email='testuser@test.com',
                password='test'
            )

        return User.objects.create_user(
            username=user_credentials['username'],
            email=user_credentials['email'],
            password=user_credentials['password']
        )

    def setUp(self):
        self.client = APIClient()
        self.user = self.get_user()
        self.token = Token.objects.create(user=self.user)
        self.url = '/api/polls/'
        self.factory = APIRequestFactory()
        self.view = PollViewSets.as_view({'post' : 'list'})

    def get_test_poll(self, poll_data=None):
        """Create a test poll and return it"""

        if not poll_data: 
            poll_data={'question': 'Test Poll Question'}

        create_response = self.client.post(
            path=self.url,
            data=poll_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        return create_response.data


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
            status.HTTP_201_CREATED,
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
            status.HTTP_401_UNAUTHORIZED,
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
            status.HTTP_401_UNAUTHORIZED,
            f'Expected status code 401(UnAuthorized access), recevied {response.status_code} instead'
        )

    def test_retreive_a_poll(self):
        """Test retrieving a specific poll"""
        poll_data = {'question': 'Test Poll'}
        test_poll = self.get_test_poll(poll_data)

        # Retreive the poll
        response = self.client.get(
            path=f'{self.url}{test_poll['id']}/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data['question'],
            poll_data['question']
        )

    def test_update_poll(self):
        """Test updating an existing poll"""

        # Create a poll
        poll_data={'question': 'Original Question'}
        test_poll = self.get_test_poll(poll_data)


        # Update the poll
        update_data={'question': 'Updated Question'}
        response = self.client.put(
            path=f'{self.url}{test_poll['id']}/',
            data=update_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['question'],
            update_data['question']
        )
    
    def test_update_nonexistence_poll(self):
        """Test upating a nonexistence poll"""
        response = self.client.put(
            path=f"{self.url}{uuid.uuid4()}/",
            data={'question': 'Updated poll question'},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_update_poll(self):
        """Test updating by unauthenticated user"""
        test_poll = self.get_test_poll()

        update_data={'question': 'Updated Question'}

        response = self.client.put(
            path=f'{self.url}{test_poll['id']}/',
            data=update_data,
            content_type='application/json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_update_poll(self):
        test_poll = self.get_test_poll()

        # Create an another test user and token for him
        user = self.get_user({'username': "test2", 'password': "test", "email": "test2user@test.com"})
        token = Token.objects.create(user=user)

        
        update_data={
            'question': 'Upadated poll'
        }

        response = self.client.put(
            path=f"{self.url}{test_poll['id']}/",
            data=update_data,
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_poll(self):
        test_poll = self.get_test_poll()

        # delete the poll 
        response = self.client.delete(
            path=f'{self.url}{test_poll['id']}/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # try to retrive that poll
        response = self.client.get(
            path=f'{self.url}{test_poll['id']}/',
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
    
    def test_unauthenticated_delete_poll(self):
        """ Test deleting poll by auauthenticated user """

        test_poll = self.get_test_poll()
        response = self.client.delete(
            path=f"{self.url}{test_poll['id']}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_delete_poll(self):
        """Test deleting by unauthorized user"""
        test_poll = self.get_test_poll()

        user2 = self.get_user(
            {'username': 'test2', 'email': 'test2user@test.com', 'password': 'test'}
        )
        token = Token.objects.create(user=user2)


        # Try to delete the poll
        response = self.client.delete(
            path=f"{self.url}{test_poll['id']}/",
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

