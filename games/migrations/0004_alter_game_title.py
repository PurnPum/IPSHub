# Generated by Django 5.0.4 on 2024-06-09 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_image_mini_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
