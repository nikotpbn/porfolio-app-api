"""
Test Artist Model Endpoints
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from portfolio import models, serializers

import tempfile
import os

from PIL import Image


def image_upload_url(id):
    """Create and return an artist image upload URL."""
    return reverse('artist-upload-image', kwargs={'pk': id})


def artist_create_list_url():
    """Create and return an artist list or create URL."""
    return reverse('artist-list')


def artist_detail_url(id):
    """Create and return an artist detail URL."""
    return reverse('artist-detail', kwargs={'pk': id})


class ArtistPrivateEndpointsTest(TestCase):
    """
    Test artist private endpoints.
    Every endpoint should work while authenticated (as admin).
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)
        self.artist = models.Artist(
            name='Test Artist',
            created_by=self.user
        )
        self.qs = models.Artist.objects.all()

    def test_artist_list(self):
        """
        Test create character list endpoint
        authenticated as admin
        """
        self.artist.save()
        res = self.client.get(artist_create_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), self.qs.count())

    def test_artist_create(self):
        """
        Test create character create endpoint
        authenticated as admin
        """
        payload = {
            'name': 'Second Artist',
            'created_by': self.user.id
        }
        res = self.client.post(artist_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.qs.count(), 1)

    def test_artist_retrieve(self):
        """
        Test create character retrieve endpoint
        authenticated as admin
        """
        self.artist.save()
        res = self.client.get(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('name', res.data)
        self.assertIn('slug', res.data)

    def test_artist_update(self):
        """
        Test create character update endpoint
        authenticated as admin
        """
        self.artist.save()
        payload = {
            'name': 'Altered Artist'
        }
        res = self.client.patch(artist_detail_url(self.artist.id), payload)

        self.artist.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.artist.name, payload['name'])

    def test_artist_delete(self):
        """
        Test create character delete endpoint
        authenticated as admin
        """
        self.artist.save()
        res = self.client.delete(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class ArtistPublicEndpointsTest(TestCase):
    """
    Test artist public endpoints.
    Only retrieve and list should work with no auth.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.artist = models.Artist(
            name='Test Artist',
            created_by=self.user
        )
        self.qs = models.Artist.objects.all()

    def test_artist_public_list(self):
        """
        Test create character list endpoint
        as an anonymous user
        """
        self.artist.save()
        res = self.client.get(artist_create_list_url())

        self.assertEqual(len(res.data), self.qs.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_artist_public_retrieve(self):
        """
        Test create character retrieve endpoint
        as an anonymous user
        """
        self.artist.save()
        res = self.client.get(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('name', res.data)
        self.assertIn('slug', res.data)

    def test_artist_public_create(self):
        """
        Test create character create endpoint
        as an anonymous user
        """
        payload = {
            'name': 'Test Artist',
            'created_by': self.user.id
        }
        res = self.client.post(artist_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_Artist_restricted_create(self):
        """
        Test create character create endpoint
        as a non admin authenticated user
        """
        self.client.force_authenticate(self.user)
        payload = {
            'name': 'Test Artist',
            'created_by': self.user.id
        }
        res = self.client.post(artist_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_artist_public_update(self):
        """
        Test create character update endpoint
        as an anonymous user
        """
        self.artist.save()
        payload = {
            'name': 'Altered Artist'
        }
        res = self.client.patch(artist_detail_url(self.artist.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, 'Test Artist')

    def test_artist_restricted_update(self):
        """
        Test create character update endpoint
        as a non admin authenticated user
        """
        self.client.force_authenticate(self.user)
        self.artist.save()
        payload = {
            'name': 'Altered Artist'
        }
        res = self.client.patch(artist_detail_url(self.artist.id), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, 'Test Artist')

    def test_artist_public_delete(self):
        """
        Test create character delete endpoint
        as an anonymous user
        """
        self.artist.save()
        res = self.client.delete(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_artist_restricted_delete(self):
        """
        Test create character delete endpoint
        as a non admin authenticated user
        """
        self.artist.save()
        self.client.force_authenticate(self.user)
        res = self.client.delete(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_artist_filter_by_name(self):
        """Test filter artists by name"""
        self.artist.save()
        another_artist = models.Artist.objects.create(
            name='Another Artist',
            created_by=self.user
        )

        s1 = serializers.ArtistSerializer(self.artist)
        s2 = serializers.ArtistSerializer(another_artist)

        params = {'name': 'Test'}
        res = self.client.get(artist_create_list_url(), params)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

        params = {'name': 'Artist'}
        res = self.client.get(artist_create_list_url(), params)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)


class ArtistImageUploadTests(TestCase):
    """Tests for the artist image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)
        self.artist = models.Artist.objects.create(
            name='Some Artist',
            created_by=self.user
        )

    def tearDown(self):
        self.artist.image.delete()

    def test_artist_image_upload(self):
        """Test uploading an image to a artist."""
        url = image_upload_url(self.artist.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.artist.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.artist.image.path))

    def test_artist_image_upload_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.artist.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
