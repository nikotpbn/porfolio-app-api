"""
Test Character Model endpoints
TODO: Test Endpoint logged in but not admin.
"""
from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from portfolio import models

from datetime import date


def character_create_list_url():
    return reverse('character-list')


def character_detail_url(id):
    return reverse('character-detail', kwargs={'pk': id})


class PrivateEndpointsTests(TestCase):
    """Test all endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='pass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_character_create(self):
        """
        Test create character create endpoint
        authenticated as admin
        """
        payload = {
            'page_id': '12345',
            'name': 'Some Comic Character',
            'sex': 'F',
            'alive': True,
            'first_appearance': date.today(),
            'created_by': self.user.id
        }
        res = self.client.post(
            character_create_list_url(),
            payload
        )
        self.assertEqual(models.Character.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_character_update(self):
        """
        Test create character update endpoint
        authenticated as admin
        """
        c = models.Character.objects.create(
            page_id='12345',
            name='Some Comic Character',
            sex='F',
            alive=True,
            first_appearance=date.today(),
            created_by=self.user
        )
        payload = {'name': 'Altered Comic Character Name'}
        res = self.client.patch(character_detail_url(c.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_character_delete(self):
        """
        Test create character delete endpoint
        authenticated as admin
        """
        c = models.Character.objects.create(
            page_id='12345',
            name='Some Comic Character',
            sex='F',
            alive=True,
            first_appearance=date.today(),
            created_by=self.user
        )
        res = self.client.delete(character_detail_url(c.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class PublicEndpointsTests(TestCase):
    """Test character public endpoints"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.c = models.Character(
            page_id='12345',
            name='Some Comic Character',
            sex='F',
            alive=True,
            first_appearance=date.today(),
            created_by=self.user
        )
        self.client = APIClient()

    def test_character_list(self):
        """
        Test create character list endpoint
        as an anonymous user
        """
        self.c.save()
        res = self.client.get(character_create_list_url())
        qs = models.Character.objects.all()

        self.assertEqual(dict(res.data[0])['slug'], self.c.slug)
        self.assertEqual(dict(res.data[0])['name'], self.c.name)
        self.assertEqual(dict(res.data[0])['sex'], self.c.sex)
        self.assertEqual(dict(res.data[0])['alive'], self.c.alive)

        self.assertEqual(len(res.data), qs.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_character_public_retrieve(self):
        """
        Test create character retrieve endpoint
        as an anonymous user
        """
        self.c.save()
        res = self.client.get(character_detail_url(self.c.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['slug'], self.c.slug)
        self.assertEqual(res.data['name'], self.c.name)
        self.assertEqual(res.data['sex'], self.c.sex)
        self.assertEqual(res.data['alive'], self.c.alive)

    def test_character_public_create(self):
        """
        Test create character create endpoint
        as an anonymous user
        """
        payload = {
            'page_id': '12345',
            'name': 'Some Comic Character',
            'sex': 'F',
            'alive': True,
            'first_appearance': date.today()
        }
        res = self.client.post(
            character_create_list_url(),
            payload
        )
        self.assertEqual(models.Character.objects.count(), 0)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_character_restricted_create(self):
        """
        Test create character create endpoint
        as a non admin authenticated user
        """
        self.client.force_authenticate(self.user)
        payload = {
            'page_id': '12345',
            'name': 'Some Comic Character',
            'sex': 'F',
            'alive': True,
            'first_appearance': date.today()
        }
        res = self.client.post(
            character_create_list_url(),
            payload
        )
        self.assertEqual(models.Character.objects.count(), 0)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_character_public_update(self):
        """
        Test create character update endpoint
        as an anonymous user
        """
        self.c.save()
        payload = {'name': 'Altered Comic Character Name'}
        res = self.client.patch(character_detail_url(self.c.id), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_character_restricted_update(self):
        """
        Test create character update endpoint
        as a non admin authenticated user
        """
        self.client.force_authenticate(self.user)
        self.c.save()
        payload = {'name': 'Altered Comic Character Name'}
        res = self.client.patch(character_detail_url(self.c.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_character_public_delete(self):
        """
        Test create character delete endpoint
        as an anonymous user
        """
        self.c.save()
        res = self.client.delete(character_detail_url(self.c.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_character_restricted_delete(self):
        """
        Test create character delete endpoint
        as a non admin authenticated user
        """
        self.client.force_authenticate(self.user)
        self.c.save()
        res = self.client.delete(character_detail_url(self.c.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
