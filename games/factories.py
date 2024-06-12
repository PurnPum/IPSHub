# games/factories.py

import random
import factory
from .models import Game

class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    title = factory.Faker('word')
    release_date = factory.Faker('date')
    developer = factory.Faker('company')
    best_emulator = factory.Faker('url')
    extra_info = factory.Faker('url')
    image_ref = factory.LazyAttribute(
        lambda o: '/static/images/pokemon_yellow_front.webp'
        if random.random() < 0.5
        else '/static/images/pokemon_crystal_front.png'
    )
