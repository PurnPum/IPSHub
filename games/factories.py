# games/factories.py

import os
import factory

from .models import Game

class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    title = factory.Faker('word')
    release_date = factory.Faker('date')
    developer = factory.Faker('company')
    best_emulator = factory.Faker('name')
    best_emulator_url = factory.Faker('url')
    type = factory.Faker('word')
    extra_info = factory.Faker('url')
    repository = factory.Faker('url')
    patch_sha = factory.Faker('word')
    patch_file_name = factory.Faker('file_name')
    image_ref = factory.Faker('random_element', elements=[
        f'static/images/{f}'
        for f in os.listdir('static/images')
        if os.path.isfile(os.path.join('static/images', f))
    ])
    image_mini_ref = factory.Faker('random_element', elements=[
        f'static/images/{f}'
        for f in os.listdir('static/images')
        if os.path.isfile(os.path.join('static/images', f))
    ])