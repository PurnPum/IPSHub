# Generated by Django 5.0.4 on 2024-09-02 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_game_patch_file_name_game_patch_sha'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='normalized_name',
            field=models.CharField(default='temp', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
