# Generated by Django 5.0.4 on 2024-08-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_game_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='patch_file_name',
            field=models.CharField(default='xd.gbc', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='patch_sha',
            field=models.CharField(default='123', max_length=100),
            preserve_default=False,
        ),
    ]
