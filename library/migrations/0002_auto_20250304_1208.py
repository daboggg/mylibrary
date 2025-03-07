from django.db import migrations, models

def save_genres(apps, schema_editor):

    with open('library/genres_list.txt', 'r') as file:
        for item in file.readlines():
            g_model = apps.get_model('library', 'Genre')
            genre_short, genre_rus = item.split('%')
            g_model(genre_short=genre_short.strip(), genre_rus=genre_rus.strip()).save()



class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(save_genres),
    ]
