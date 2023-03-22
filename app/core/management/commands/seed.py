"""
Django command to seed initital data
"""
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from portfolio.models import Tag, Character
from datetime import date
import json


class Command(BaseCommand):
    """Django command to read files and populate data"""

    def handle(self, *args, **options):
        """Entrypoint for command"""

        self.create_characters()
        self.create_tags()
        # self.create_artists(data['artists'])

        self.stdout.write(self.style.SUCCESS('Seeding Finished!'))

    def create_characters(self):

        data = {}
        with open('/app/core/seed_data/characters.json', 'r') as file:
            data = json.load(file)

        for obj in data:
            try:
                character = Character.objects.get(name=obj['name'])
                self.stdout.write(
                    f'Character {character.name} already exists, \
                    skipping creation...'
                )

            except ObjectDoesNotExist:
                obj['first_appearance'] = date(
                    int(obj['first_appearance']), 1, 1
                )
                character = Character.objects.create(**obj)
                self.stdout.write(f'Creating Character Object: \
                                  {character.name}')

        self.stdout.write(self.style.SUCCESS('Finished seeding characters.'))

    def create_tags(self):
        data = {}
        with open('/app/core/seed_data/tags.json', 'r') as file:
            data = json.load(file)

        for obj in data:
            tag, created = Tag.objects.get_or_create(**obj)

            if not created:
                self.stdout.write(
                    f'Tag {tag.name} already exists, skipping creation...'
                )
            else:
                self.stdout.write(f'Creating Tag Object: {tag.name}')
