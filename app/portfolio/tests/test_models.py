"""
Tests for portfolio models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from portfolio import models

from unittest.mock import patch

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
            first_appearance=date.today(),
            created_by=self.user
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
                first_appearance=date.today(),
                created_by=self.user
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

    def test_artist_creation_name_and_slug(self):
        """Test normalize_name on Artist .save method"""
        samples = [
            ['ChaRacTer OnE ', 'Character One', 'character-one'],
            [' cHaRaCteR tWO ', 'Character Two', 'character-two'],
            [' chAraCtER THREe ', 'Character Three', 'character-three'],
        ]

        for name, expected_name, expected_slug in samples:
            artist = models.Artist.objects.create(
                name=name,
                created_by=self.user
            )
            self.assertEqual(artist.name, expected_name)
            self.assertEqual(artist.slug, expected_slug)

    def test_art_creation_title_and_subtitle(self):
        """Test normalize_name on Art .save method"""
        samples = [
            ['ArT OnE ', 'Art One',
             'aRT oNe SubTiTLE ', 'Art One Subtitle'],
            [' ArT TWO', 'Art Two',
             ' aRT tWO SuBtItlE', 'Art Two Subtitle'],
            [' ArT thrEE ', 'Art Three',
             ' aRT THREe SUBTiTLE ', 'Art Three Subtitle'],
        ]
        artist = models.Artist.objects.create(
            name='Test Artist',
            created_by=self.user
        )

        for title, expected_title, subtitle, expected_subtitle in samples:
            art = models.Art.objects.create(
                title=title,
                subtitle=subtitle,
                type=1,
                artist=artist,
                created_by=self.user
            )
            self.assertEqual(art.title, expected_title)
            self.assertEqual(art.subtitle, expected_subtitle)

    @patch('portfolio.models.uuid.uuid4')
    def test_artist_file_name_uuid(self, mock_uuid):
        """Test generating artist image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.artist_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/artist/{uuid}.jpg')

    @patch('portfolio.models.uuid.uuid4')
    def test_art_filename_uuid(self, mock_uuid):
        """Test generating art image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.art_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/art/{uuid}.jpg')
