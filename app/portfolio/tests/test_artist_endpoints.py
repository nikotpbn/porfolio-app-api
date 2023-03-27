"""
Test Artist Model Endpoints
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from portfolio import models


def artist_create_list_url():
    return reverse('portfolio:artist-list')


def artist_detail_url(id):
    return reverse('portfolio:artist-detail', kwargs={'pk': id})


class ArtistPrivateEndpointsTest(TestCase):
    """
    Test artist private endpoints.
    Every endpoint should work while authenticated.
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
        """Test artist list endpoint."""
        self.artist.save()
        res = self.client.get(artist_create_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), self.qs.count())

    def test_artist_create(self):
        """Test artist create endpoint."""
        payload = {
            'name': 'Second Artist',
            'created_by': self.user.id
        }
        res = self.client.post(artist_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.qs.count(), 1)

    def test_artist_retrieve(self):
        """Test artist retrieve endpoint."""
        self.artist.save()
        res = self.client.get(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('name', res.data)
        self.assertIn('slug', res.data)

    def test_artist_update(self):
        """Test artist update endpoint."""
        self.artist.save()
        payload = {
            'name': 'Altered Artist'
        }
        res = self.client.patch(artist_detail_url(self.artist.id), payload)

        self.artist.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.artist.name, payload['name'])

    def test_artist_delete(self):
        """Test artist delete endpoint."""
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
        self.artist.save()
        res = self.client.get(artist_create_list_url())

        self.assertEqual(len(res.data), self.qs.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_artist_public_retrieve(self):
        self.artist.save()
        res = self.client.get(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('name', res.data)
        self.assertIn('slug', res.data)

    def test_artist_public_create(self):
        payload = {
            'name': 'Test Artist',
            'created_by': self.user.id
        }
        res = self.client.post(artist_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_artist_public_update(self):
        self.artist.save()
        payload = {
            'name': 'Altered Artist'
        }
        res = self.client.patch(artist_detail_url(self.artist.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, 'Test Artist')

    def test_artist_public_delete(self):
        self.artist.save()
        res = self.client.delete(artist_detail_url(self.artist.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
