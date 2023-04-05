"""
Tests on all tag endpoints
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from portfolio import models


def get_tag_list_create_url():
    return reverse('tag-list')


def get_tag_detail_url(id):
    return reverse('tag-detail', kwargs={'pk': id})


class TagEndpointsTests(TestCase):
    """Test private tag endpoints"""
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()

        self.t = models.Tag(
            name='Test Tag',
            description='Test tag description',
            created_by=self.user
        )

    def test_list_tags_success(self):
        """Test list tags end points while logged in as admin."""
        self.client.force_authenticate(self.user)
        self.t.save()
        res = self.client.get(get_tag_list_create_url())

        qs = models.Tag.objects.all()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(qs.count(), len(res.data))
        self.assertEqual(res.data[0]['name'], 'Test Tag')
        self.assertEqual(res.data[0]['description'], 'Test tag description')
        self.assertEqual(res.data[0]['created_by'], self.user.id)

    def test_create_tag_success(self):
        """Test creating a tag while logged in as admin."""
        self.client.force_authenticate(self.user)
        payload = {
            'name': 'Test Tag',
            'description': 'Test tag description',
            'created_by': self.user.id
        }
        res = self.client.post(get_tag_list_create_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_edit_tag_success(self):
        """Test editing a tag while logged in as admin."""
        self.client.force_authenticate(self.user)
        self.t.save()
        payload = {
            'pk': self.t.id,
            'name': 'Altered Tag Name'
        }
        res = self.client.patch(get_tag_detail_url(self.t.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_tag_success(self):
        """Test deleting a tag while logged in as admin."""
        self.client.force_authenticate(self.user)
        self.t.save()
        res = self.client.delete(get_tag_detail_url(self.t.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_tags_unauthorized(self):
        """Test list tags as an anonymous user."""
        self.t.save()
        res = self.client.get(get_tag_list_create_url())
        self.assertIn('detail', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tags_unauthorized(self):
        """Test create tags as an anonymous user."""
        payload = {
            'name': 'Test Tag',
            'description': 'Test tag description',
            'created_by': self.user.id
        }
        res = self.client.post(get_tag_list_create_url(), payload)
        self.assertIn('detail', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_tags_unauthoriized(self):
        """Test edit tags as an anonymous user."""
        self.t.save()
        payload = {
            'pk': self.t.id,
            'name': 'Altered Tag Name'
        }
        res = self.client.patch(get_tag_detail_url(self.t.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_tags_unauthorized(self):
        """Test delete tags as an anonymous user."""
        self.t.save()
        res = self.client.delete(get_tag_detail_url(self.t.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
