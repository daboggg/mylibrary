# Generated by Django 5.1.6 on 2025-04-06 10:00

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('nickname', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('home_pages', models.CharField(blank=True, max_length=500, null=True)),
                ('emails', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_short', models.CharField(max_length=50)),
                ('genre_rus', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('lat_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('annotation', models.TextField(blank=True, null=True)),
                ('book_file', models.FileField(upload_to='books/')),
                ('coverpage', models.ImageField(blank=True, null=True, upload_to='coverpages/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ManyToManyField(blank=True, related_name='books', to='library.author')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('genres', models.ManyToManyField(blank=True, related_name='books', to='library.genre')),
                ('sequence', models.ManyToManyField(blank=True, related_name='books', to='library.sequence')),
            ],
        ),
    ]
