# Generated by Django 5.0.4 on 2024-08-09 11:19

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patches', '0013_alter_patchdata_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiffFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('filename', models.CharField(max_length=200)),
                ('original_file', models.CharField(max_length=200)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patches.pofield')),
            ],
        ),
    ]
