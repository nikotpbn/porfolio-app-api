# Generated by Django 4.1.7 on 2023-03-17 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('alive', models.BooleanField()),
                ('first_appearance', models.DateField()),
            ],
        ),
    ]
