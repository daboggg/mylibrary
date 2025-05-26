from django.contrib.auth.hashers import make_password
from django.db import migrations, models
from pytils.translit import slugify


def save_genres(apps, schema_editor):

    with open('library/genres_list.txt', 'r') as file:
        for item in file.readlines():
            g_model = apps.get_model('library', 'Genre')
            genre_short, genre_rus = item.split('%')
            g_model(genre_short=genre_short.strip(), genre_rus=genre_rus.strip(), slug=slugify(genre_rus.strip())).save()

def add_user1(apps, schema_editor):
    model = apps.get_model('users', 'User')
    model.objects.create(username='admin', is_superuser=True, email='daboggg@ya.ru', password=make_password('As144911.'))

class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(save_genres),
        migrations.RunPython(add_user1),
    ]
