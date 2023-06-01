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
            'core.management.commands.seed.Command.create_dc_characters',
            return_value='Finished DC characters seed.'
    )
    def test_dc_character_seed_command(self, patched_character_creation_fnc):
        self.assertEqual(
            patched_character_creation_fnc.return_value,
            'Finished DC characters seed.'
        )

    @patch(
            'core.management.commands.seed.Command.create_marvel_characters',
            return_value='Finished Marvel characters seed.'
    )
    def test_marv_character_seed_command(self, patched_character_creation_fnc):
        self.assertEqual(
            patched_character_creation_fnc.return_value,
            'Finished Marvel characters seed.'
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
