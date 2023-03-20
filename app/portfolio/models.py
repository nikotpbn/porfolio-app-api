from django.db import models
from django.utils.timezone import now # noqa
from django.utils.text import slugify

import uuid
import os


def image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "    {}.{}".format(uuid.uuid4().hex, ext)
    upload_path = os.path.join('uploads', 'image', filename)

    return upload_path


class Character(models.Model):

    class Sex(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    page_id = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    sex = models.CharField(max_length=1, choices=Sex.choices)
    alive = models.BooleanField()
    first_appearance = models.DateField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
