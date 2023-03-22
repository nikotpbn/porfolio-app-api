from django.db import models
from django.utils.timezone import now # noqa
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import uuid
import os


def image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "    {}.{}".format(uuid.uuid4().hex, ext)
    upload_path = os.path.join('uploads', 'image', filename)

    return upload_path


def normalize_name(str):
    return str.lower().strip().title()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='tags'
    )

    def __str__(self):
        return self.name

    def save(self):
        self.name = normalize_name(self.name)


class Character(models.Model):

    class Sex(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    page_id = models.CharField(max_length=10)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    sex = models.CharField(max_length=1, choices=Sex.choices)
    alive = models.BooleanField()
    first_appearance = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = normalize_name(self.name)
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
