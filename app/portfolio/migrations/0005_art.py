# Generated by Django 4.1.7 on 2023-03-28 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import portfolio.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0004_artist_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('subtitle', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=portfolio.models.image_file_path)),
                ('type', models.IntegerField(choices=[(1, 'Drawing'), (2, 'Painting'), (3, 'Sculpture'), (4, 'Tatoo'), (5, 'Photo'), (6, 'Digital')])),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks', to='portfolio.artist')),
                ('characters', models.ManyToManyField(to='portfolio.character')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='portfolio.tag')),
            ],
        ),
    ]
