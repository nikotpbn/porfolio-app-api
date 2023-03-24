"""
Tests for portfolio models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from portfolio import models

from datetime import date


class PortfolioModelsTests(TestCase):
    """Test Models."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='Test USer',
            email='test@example.com',
            password='testpass123',
        )

    def test_character_creation_and_editing_slug(self):
        """Test slugfy function on character .save method"""
        character = models.Character.objects.create(
            page_id='12345',
            name='Some Comic Character',
            sex='F',
            alive=True,
            first_appearance=date.today()
        )

        self.assertEqual(character.slug, 'some-comic-character')

        character.name = 'Altered Character Name'
        character.save()
        character.refresh_from_db()

        self.assertEqual(character.slug, 'altered-character-name')

    def test_character_creation_name(self):
        """Test normalize_name on character .save method"""
        sample_names = [
            [' ChaRacter ONE NamE', 'Character One Name'],
            ['CHARACTER twO NAME ', 'Character Two Name'],
            [' character ThreE NAME ', 'Character Three Name']
        ]

        for name, expected in sample_names:
            character = models.Character.objects.create(
                page_id='12345',
                name=name,
                sex='F',
                alive=True,
                first_appearance=date.today()
            )
            self.assertEqual(character.name, expected)

    def test_tag_creation_name(self):
        """Test normalize_name on tag .save method"""
        sample_names = [
            ['TAG ONe ', 'Tag One'],
            [' tAG tWO', 'Tag Two'],
            [' tag THREE ', 'Tag Three']
        ]

        for name, expected in sample_names:
            tag = models.Tag.objects.create(
                name=name,
                description="Some Tag description",
                created_by=self.user
            )
            self.assertEqual(tag.name, expected)
