# Generated by Django 5.1.6 on 2025-03-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_book_coverpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
