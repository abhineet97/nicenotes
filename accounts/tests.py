from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer

User = get_user_model()

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('1234567890', 'thisisapassword', full_name='Test_User')
        self.test_user_token = Token.objects.create(user=self.test_user).key
        self.users_url = reverse('user-list')
        self.current_user_url = reverse('user-detail')
        self.token_url = reverse('api-token')

    def test_create_user(self):
        data = {
                'mobile': '0987654321',
                'full_name': 'Awersome Tester',
                'password': 'notatallweakpass',
                }

        response = self.client.post(self.users_url, data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['mobile'], data['mobile'])
        self.assertEqual(response.data['full_name'], data['full_name'])
        self.assertFalse('password' in response.data)
        self.assertEqual(response.data['token'], token.key)

    def test_list_users(self):
        user1 = User.objects.create_user('0987654321', 'passingthepass', full_name='Dope Tester')
        user2 = User.objects.create_user('1234509876', 'passthesauceplease', full_name='Happy Tester')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token)
        response = self.client.get(self.users_url)
        users = User.objects.all().exclude(auth_token=self.test_user_token)

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.data, UserSerializer(users, many=True).data)
        self.assertFalse('view_access_to' in response.data)
        self.assertFalse('edit_access_to' in response.data)
        

    def test_user_login(self):
        data = {
                'username': '1234567890',
                'password': 'thisisapassword'
                }
        response = self.client.post(self.token_url, data, format='json')
        token = Token.objects.get(user=self.test_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token.key)

    def test_notes_shared_with_current_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token)
        response = self.client.get(self.current_user_url)

        serialized = UserSerializer(User.objects.get(auth_token=self.test_user_token), show_access_only=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)
