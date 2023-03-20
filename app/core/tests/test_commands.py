"""
Test custom Django management commands
"""

from unittest.mock import patch, mock_open

from MySQLdb import OperationalError as MySQLError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperatinalErrro."""
        patched_check.side_effect = [MySQLError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

    def test_seed_data_files(self, patched_check):
        with patch('builtins.open', mock_open(read_data='tags_file')) as m:
            with open('/app/core/seed_data/tags.json') as h:
                result = h.read()

        m.assert_called_once_with('/app/core/seed_data/tags.json')
        self.assertEqual(result, 'tags_file')
