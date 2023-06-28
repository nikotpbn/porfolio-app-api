"""
Django custom command to seed initital data
"""
from django.core.management.base import BaseCommand, CommandParser
from django.core.exceptions import ObjectDoesNotExist
from portfolio.models import Tag, Character, Artist
from datetime import date
import json

from core.utils import normalize_name

from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Django command to read files and populate data
    use: python manage.py seed --show [ True | False ]
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--show', type=bool, required=False)
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.admin = get_user_model().objects.get(id=1)

        if self.admin.is_superuser:
            self.create_dc_characters(options['show'])
            self.create_marvel_characters(options['show'])
            self.create_artists(options['show'])
            self.create_tags(options['show'])

            self.stdout.write(self.style.SUCCESS("Seeding Finished!"))
        else:
            self.stdout.wirte(self.style.ERROR("There is no admin user."))

    def create_tags(self, show):
        data = {}
        with open("/app/core/seed_data/tags.json", "r") as file:
            data = json.load(file)

        for obj in data:
            try:
                tag = Tag.objects.get(name=obj['name'])
                if show:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Tag {tag.name} already exists, \
                        skipping creation..."
                        )
                    )
            except ObjectDoesNotExist:
                obj["created_by"] = self.admin
                tag = Tag.objects.create(**obj)
                if show:
                    self.stdout.write(
                        f"Creating Tag Object: \
                                    {obj.name}"
                    )

        self.stdout.write(
            self.style.SUCCESS("Finished seeding tags.")
        )

    def create_artists(self, show):
        data = {}
        with open("/app/core/seed_data/artists.json", "r") as file:
            data = json.load(file)

        for obj in data:
            try:
                name = normalize_name(obj["name"])
                artist = Artist.objects.get(name=name)
                if show:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Artist {artist.name} already exists, \
                        skipping creation..."
                        )
                    )
            except ObjectDoesNotExist:
                obj["created_by"] = self.admin
                artist = Artist.objects.create(**obj)
                if show:
                    self.stdout.write(
                        f"Creating Artist Object: \
                                    {obj.name}"
                    )

        self.stdout.write(
            self.style.SUCCESS("Finished seeding artists.")
        )

    def create_dc_characters(self, show):
        data = {}
        with open("/app/core/seed_data/dc_characters.json", "r") as file:
            data = json.load(file)

        for obj in data:
            try:
                character = Character.objects.get(name=obj["name"])
                if show:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Character {character.name} already exists, \
                        skipping creation..."
                        )
                    )

            except ObjectDoesNotExist:
                obj["first_appearance"] = date(
                    int(obj["first_appearance"]),
                    1, 1
                )
                obj["created_by"] = self.admin
                character = Character.objects.create(**obj)
                if show:
                    self.stdout.write(
                        f"Creating Character Object: \
                                    {character.name}"
                    )

        self.stdout.write(
            self.style.SUCCESS("Finished seeding DC characters.")
        )

    def create_marvel_characters(self, show):
        with open("/app/core/seed_data/marvel_characters.json", "r") as file:
            data = json.load(file)

        for obj in data:
            try:
                character = Character.objects.get(name=obj["name"])
                if show:
                    self.stdout.write(
                        f"Character {character.name} \
                            already exists, skipping creation..."
                    )
            except ObjectDoesNotExist:
                obj["first_appearance"] = date(
                    int(obj["first_appearance"]),
                    1, 1
                )
                obj["created_by"] = self.admin
                character = Character.objects.create(**obj)
                if show:
                    self.stdout.write(
                        f"Creating Charater Object: {character.name}"
                    )

        self.stdout.write(
            self.style.SUCCESS("Finished seeding Marvel characters.")
        )
