from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import uuid
import os


def art_image_file_path(instance, filename):
    """Generate file path for new art image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'art', filename)


def artist_image_file_path(instance, filename):
    """Generate file path for new artist image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'artist', filename)


def normalize_name(str):
    """Auxiliar function to captalize the first letters of a name"""
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

    def save(self, *args, **kwargs):
        self.name = normalize_name(self.name)
        return super().save(*args, **kwargs)


class Character(models.Model):

    class Sex(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    page_id = models.CharField(max_length=10)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    sex = models.CharField(max_length=1, choices=Sex.choices)
    alive = models.BooleanField()
    first_appearance = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = normalize_name(self.name)
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=artist_image_file_path
    )
    instagram = models.CharField(max_length=128, blank=True, null=True)
    deviant = models.CharField(max_length=128, blank=True, null=True)
    twitter = models.CharField(max_length=128, blank=True, null=True)
    oficial = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = normalize_name(self.name)
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Art(models.Model):
    TYPE_CHOICES = [
        (1, 'Drawing'),
        (2, 'Painting'),
        (3, 'Sculpture'),
        (4, 'Tatoo'),
        (5, 'Photo'),
        (6, 'Digital')
    ]

    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=art_image_file_path)
    type = models.IntegerField(choices=TYPE_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='artworks'
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = normalize_name(self.title)
        self.subtitle = normalize_name(self.subtitle)
        return super().save(*args, **kwargs)
