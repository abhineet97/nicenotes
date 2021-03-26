from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Note
from .serializers import NoteSerializer

User = get_user_model()


class NoteTest(APITestCase):
    def setUp(self):
        self.list_url = reverse("note-list")
        self.test_user = User.objects.create_user(
            "1234567890", "thisisapassword", full_name="Test User"
        )
        self.test_user1 = User.objects.create_user(
            "0987654321", "sosecurepassword", full_name="Another User"
        )
        self.token = Token.objects.create(user=self.test_user)
        self.token1 = Token.objects.create(user=self.test_user1)
        self.setToken(self.token.key)

    def setToken(self, token_key):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)

    def test_list_notes_of_current_user(self):
        Note.objects.create(content="TESTING TESTING 123", owner=self.test_user)
        Note.objects.create(content="TESTING TESTING 456", owner=self.test_user)

        # create a note by different user
        Note.objects.create(content="TESTING TESTING 789", owner=self.test_user1)

        response = self.client.get(self.list_url, format="json")
        notes = Note.objects.filter(owner=self.test_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, NoteSerializer(notes, many=True).data)

    def test_create_new_note_for_current_user(self):
        data = {"content": "YOLOLOLOL"}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], data["content"])

    def test_update_content_of_existing_note_for_current_user(self):
        note = Note.objects.create(content="Something", owner=self.test_user)

        data = {"content": "NONONONONNO"}
        url = reverse("note-detail", kwargs={"pk": note.id})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], data["content"])

    def test_provide_edit_access(self):
        note = Note.objects.create(content="Something", owner=self.test_user)

        data = {"edit_access_to": [self.test_user1.id]}
        url = reverse("note-detail", kwargs={"pk": note.id})

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["edit_access_to"], data["edit_access_to"])
