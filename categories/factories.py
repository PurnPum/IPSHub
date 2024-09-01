# categories/factories.py

import factory
from .models import Category
from games.factories import GameFactory

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    base_game = factory.SubFactory(GameFactory)
    description = factory.Faker('paragraph')
    image_ref = factory.Faker('url')
    name = factory.Faker('word')