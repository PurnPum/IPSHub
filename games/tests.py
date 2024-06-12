from django.test import TransactionTestCase
from .models import Game
from .factories import GameFactory
from categories.factories import CategoryFactory

class GameTestCase(TransactionTestCase):

    def setUp(self):
        self.game = GameFactory()
        self.category1 = CategoryFactory(base_game=self.game)
        self.category2 = CategoryFactory(base_game=self.game)

    def test_game_creation(self):
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(self.game.categories.count(), 2)

    def test_categories(self):
        categories = self.game.categories.all()
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

