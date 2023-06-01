"""
Django custom command to seed initital data
"""
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from portfolio.models import Tag, Character
from datetime import date
import json

from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """Django command to read files and populate data"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.admin = get_user_model().objects.get(id=1)

        if self.admin.is_superuser:
            self.create_dc_characters()
            self.create_marvel_characters()
            self.create_tags()
            # self.create_artists(data['artists'])

            self.stdout.write(self.style.SUCCESS("Seeding Finished!"))
        else:
            self.stdout.wirte(self.style.ERROR("User is not admin."))

    def create_dc_characters(self):
        data = {}
        with open("/app/core/seed_data/dc_characters.json", "r") as file:
            data = json.load(file)

        for obj in data:
            try:
                character = Character.objects.get(name=obj["name"])
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
                self.stdout.write(
                    f"Creating Character Object: \
                                  {character.name}"
                )

        self.stdout.write(
            self.style.SUCCESS("Finished seeding DC characters.")
        )

    def create_marvel_characters(self):
        with open("/app/core/seed_data/marvel_characters.json", "r") as file:
            data = json.load(file)

        for obj in data:
            try:
                character = Character.objects.get(name=obj["name"])
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
                self.stdout.write(
                    f"Creating Charater Object: {character.name}"
                )

        self.stdout.write(
            self.style.SUCCESS("Finished seeding DC characters.")
        )

    def create_tags(self):
        data = {}
        with open("/app/core/seed_data/tags.json", "r") as file:
            data = json.load(file)

        for obj in data:
            tag, created = Tag.objects.get_or_create(**obj)

            if not created:
                self.stdout.write(
                    f"Tag {tag.name} already exists, skipping creation..."
                )
            else:
                self.stdout.write(f"Creating Tag Object: {tag.name}")
