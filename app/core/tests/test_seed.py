"""
Test custom Django management commands
"""
from unittest.mock import patch, mock_open
from django.test import SimpleTestCase


class SeedTests(SimpleTestCase):
    """Test data files and command."""

    def test_seed_data_files(self):
        with patch('builtins.open', mock_open(read_data='tags_file')) as m:
            with open('/app/core/seed_data/tags.json') as h:
                result = h.read()
        m.assert_called_once_with('/app/core/seed_data/tags.json')
        self.assertEqual(result, 'tags_file')

        with patch('builtins.open',
                   mock_open(read_data='characters_file')
                   ) as m:
            with open('/app/core/seed_data/characters.json') as h:
                result = h.read()
        m.assert_called_once_with('/app/core/seed_data/characters.json')
        self.assertEqual(result, 'characters_file')

        with patch('builtins.open', mock_open(read_data='artists_file')) as m:
            with open('/app/core/seed_data/artists.json') as h:
                result = h.read()
        m.assert_called_once_with('/app/core/seed_data/artists.json')
        self.assertEqual(result, 'artists_file')

    @patch(
            'core.management.commands.seed.Command.create_characters',
            return_value='Finished characters seed.'
    )
    def test_character_seed_command(self, patched_create_characters):
        self.assertEqual(
            patched_create_characters.return_value,
            'Finished characters seed.'
        )

    @patch(
            'core.management.commands.seed.Command.create_tags',
            return_value='Finished seeding tags.'
    )
    def test_tag_seed_command(self, patched_create_tags):
        self.assertEqual(
            patched_create_tags.return_value,
            'Finished seeding tags.'
        )
