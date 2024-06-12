from django.test import TransactionTestCase
from .models import Category
from .factories import CategoryFactory
from games.factories import GameFactory

class CategoryTestCase(TransactionTestCase):

    def setUp(self):
        self.game = GameFactory()
        self.parent_category = CategoryFactory(base_game=self.game)
        self.sub_category1 = CategoryFactory(base_game=self.game, parent_category=self.parent_category)
        self.sub_category2 = CategoryFactory(base_game=self.game, parent_category=self.parent_category)

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(self.parent_category.subcategories.count(), 2)

    def test_subcategories(self):
        subcategories = self.parent_category.subcategories.all()
        self.assertIn(self.sub_category1, subcategories)
        self.assertIn(self.sub_category2, subcategories)

    def test_game_relationship(self):
        self.assertEqual(self.parent_category.base_game, self.game)
        self.assertEqual(self.sub_category1.base_game, self.game)
        self.assertEqual(self.sub_category2.base_game, self.game)
