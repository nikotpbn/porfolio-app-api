from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from portfolio.models import Tag, TagGroup, Character, Artist
from datetime import date
import json
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = {}

        # Load data into memory
        self.stdout.write("seeding data...")
        with open(f'{os.getcwd()}/seed_data/characters.json', 'r') as file:
            data['characters'] = json.load(file)

        with open(f'{os.getcwd()}/seed_data/tag_groups.json', 'r') as file:
            data['tag_groups'] = json.load(file)

        with open(f'{os.getcwd()}/seed_data/tags.json', 'r') as file:
            data['tags'] = json.load(file)

        with open(f'{os.getcwd()}/seed_data/artists.json', 'r') as file:
            data['artists'] = json.load(file)

        self.create_characters(self, data['characters'])
        self.create_tag_groups(data['tag_groups'])
        self.create_tags(data['tags'])
        self.create_artists(data['artists'])

        self.stdout.write("seeding finished.")

    def create_characters(self, data):
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

    def create_tag_groups(self, data):
        for obj in data:
            tag_group, created = TagGroup.objects.get_or_create(
                name=obj['name']
            )
            if not created:
                self.stdout.write(
                    f'TagGroup {tag_group.name} already exists, \
                    skipping creation...'
                )
            else:
                self.stdout.write(f'Creating TagGroup Object: \
                                  {tag_group.name}')

    def create_tags(self, data):
        for obj in data:
            obj['group'] = TagGroup.objects.get(id=obj['group'])
            tag, created = Tag.objects.get_or_create(**obj)

            if not created:
                self.stdout.write(
                    f'Tag {tag.name} already exists, skipping creation...'
                )
            else:
                self.stdout.write(f'Creating Tag Object: {tag.name}')

    def create_artists(self, data):
        # TODO: Clean URLs of query string param on JSON file
        for obj in data:
            artist, created = Artist.objects.get_or_create(**obj)

            if not created:
                self.stdout.write(
                    f'Artist {artist} already exists, skipping creation...'
                )
            else:
                self.stdout.write(f'Creating Artist object: {artist.name}')
