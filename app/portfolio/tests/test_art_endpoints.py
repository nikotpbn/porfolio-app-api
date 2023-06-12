from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from portfolio import models
from portfolio.api import serializers

import tempfile
import os

from PIL import Image


def image_upload_url(id):
    """Create and return an art image upload URL."""
    return reverse('art-upload-image', kwargs={'pk': id})


def art_create_list_url():
    """Create and return an art list or create URL."""
    return reverse('art-list')


def art_detail_url(id):
    """Create and return an art detail URL."""
    return reverse('art-detail', kwargs={'pk': id})


class ArtPrivateEndpointsTests(TestCase):
    """Test all private Art endpoints"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testpass123'
        )
        self.artist = models.Artist.objects.create(
            name='Test Artist',
            created_by=self.user
        )
        self.art = models.Art(
            title='Test Art Title',
            subtitle='Test Art Subtitle',
            type=1,
            artist=self.artist,
            created_by=self.user
        )
        self.client.force_authenticate(self.user)
        self.qs = models.Art.objects.all()

    def test_art_list_endpoint(self):
        """Test art List endpoint"""
        self.art.save()
        res = self.client.get(art_create_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), self.qs.count())

    def test_art_retrieve_endpoint(self):
        self.art.save()
        res = self.client.get(art_detail_url(self.art.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('title', res.data)

    def test_art_create_endpoint(self):
        """Test art create endpoint"""
        tag = models.Tag.objects.create(
            name='Test Tag',
            description='Tag Description',
            created_by=self.user
        )
        tag2 = models.Tag.objects.create(
            name='Test Tag Two',
            description='Tag Description',
            created_by=self.user
        )
        payload = {
            'title': 'Test Art Title',
            'subtitle': 'Test Art Subtitle',
            'type': 1,
            'artist': self.artist.id,
            'created_by': self.user.id,
            'tags': [tag.id, tag2.id]
        }
        res = self.client.post(art_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['subtitle'], payload['subtitle'])
        self.assertEqual(res.data['type'], payload['type'])

    def test_art_update_endpoint(self):
        """Test art update endpoint"""
        self.art.save()
        payload = {
            'title': 'Altered Art Title',
            'subtitle': 'Altered Art Subtitle',
            'type': 2
        }
        res = self.client.patch(art_detail_url(self.art.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['subtitle'], payload['subtitle'])
        self.assertEqual(res.data['type'], payload['type'])

    def test_art_delete_endpoint(self):
        """Test art delete endpoint."""
        self.art.save()
        res = self.client.delete(art_detail_url(self.art.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class ArtPublicEndpointsTest(TestCase):
    """
    Test art public endpoints
    Only list and retrieve should be available
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.artist = models.Artist.objects.create(
            name='Test Artist',
            created_by=self.user
        )
        self.art = models.Art(
            title='Test Art Title',
            subtitle='Test Art Subtitle',
            type=1,
            artist=self.artist,
            created_by=self.user
        )
        self.qs = models.Art.objects.all()

    def test_art_list_public_endpoints(self):
        self.art.save()
        res = self.client.get(art_create_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), self.qs.count())

    def test_art_retrieve_public_endpoint(self):
        self.art.save()
        res = self.client.get(art_detail_url(self.art.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('title', res.data)
        self.assertIn('subtitle', res.data)
        self.assertIn('type', res.data)
        self.assertIn('artist', res.data)
        self.assertIn('created_by', res.data)

    def test_art_create_public_endpoint(self):
        payload = {
            'title': 'Test Art Title',
            'subtitle': 'Test Art Subtitle',
            'type': 1,
            'artist': self.artist.id,
            'created_by': self.user.id,
        }
        res = self.client.post(art_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_art_create_restricted_endpoint(self):
        self.client.force_authenticate(self.user)
        payload = {
            'title': 'Test Art Title',
            'subtitle': 'Test Art Subtitle',
            'type': 1,
            'artist': self.artist.id,
            'created_by': self.user.id,
        }
        res = self.client.post(art_create_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_art_update_public_endpoint(self):
        self.art.save()
        payload = {
            'title': 'Altered Art Title',
            'subtitle': 'Altered Art Subtitle',
            'type': 2
        }
        res = self.client.patch(art_detail_url(self.art.id), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_art_update_restricted_endpoint(self):
        self.client.force_authenticate(self.user)
        self.art.save()
        payload = {
            'title': 'Altered Art Title',
            'subtitle': 'Altered Art Subtitle',
            'type': 2
        }
        res = self.client.patch(art_detail_url(self.art.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_art_delete_public_endpoint(self):
        self.art.save()
        res = self.client.delete(art_detail_url(self.art.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_art_delete_restricted_endpoint(self):
        self.client.force_authenticate(self.user)
        self.art.save()
        res = self.client.delete(art_detail_url(self.art.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_art_filter_by_tags(self):
        """Test filtering art by tags"""
        self.art.save()
        another_artist = models.Artist.objects.create(
            name='Another Artist',
            created_by=self.user
        )
        another_art = models.Art.objects.create(
            title='Another Art Title',
            subtitle='Another Art Subtitle',
            type=1,
            artist=another_artist,
            created_by=self.user
        )
        tag = models.Tag.objects.create(
            name='Tag One',
            description='Tag One Description',
            created_by=self.user
        )
        self.art.tags.add(tag)

        params = {'tags': f'{tag.id}'}
        res = self.client.get(art_create_list_url(), params)

        s1 = serializers.ArtSerializer(self.art)
        s2 = serializers.ArtSerializer(another_art)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(s1.data, res.data['results'])
        self.assertNotIn(s2.data, res.data['results'])

    def test_art_filter_by_artist(self):
        """Test filtering art by artist"""
        self.art.save()
        another_art = models.Art.objects.create(
            title='Another Art Title',
            subtitle='Another Art Subtitle',
            type=1,
            artist=self.artist,
            created_by=self.user
        )
        alternative_artist = models.Artist.objects.create(
            name='Another Artist',
            created_by=self.user
        )
        alternative_art = models.Art.objects.create(
            title='Another Art Title',
            subtitle='Another Art Subtitle',
            type=1,
            artist=alternative_artist,
            created_by=self.user
        )

        params = {'artists': f'{self.artist.id}'}
        res = self.client.get(art_create_list_url(), params)

        s1 = serializers.ArtSerializer(self.art)
        s2 = serializers.ArtSerializer(another_art)
        s3 = serializers.ArtSerializer(alternative_art)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(s1.data, res.data['results'])
        self.assertIn(s2.data, res.data['results'])
        self.assertNotIn(s3.data, res.data['results'])


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)
        self.artist = models.Artist.objects.create(
            name='Test Artist',
            created_by=self.user
        )
        self.art = models.Art.objects.create(
            title='Test Art Title',
            subtitle='Test Art Subtitle',
            type=1,
            artist=self.artist,
            created_by=self.user
        )

    def tearDown(self):
        """Test uploading an image to a art."""
        self.art.image.delete()

    def test_art_image_upload(self):
        """Test uploading an image to a art."""
        url = image_upload_url(self.art.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.art.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.art.image.path))

    def test_art_image_upload_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.art.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
