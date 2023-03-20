"""
Tests for portfolio models.
"""
from django.test import TestCase
from portfolio import models

from datetime import date


class PortfolioModelsTests(TestCase):
    """Test Models."""

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
