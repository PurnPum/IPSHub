from django.test import TestCase
from games.models import Game
from core.add_real_data_to_db import add_data_to_bd

class GameTestCase(TestCase):

    def setUp(self):
        add_data_to_bd()
        self.test_game = Game.objects.get(title='Pokémon Yellow')

    def test_game_creation(self):
        self.assertEqual(Game.objects.count(), 4)
        
    def test_title(self):
        self.assertEqual(str(self.test_game), 'Pokémon Yellow')
    
    def test_game_functions_get_patches(self):
        print(self.test_game.get_patches())
        self.assertEqual(self.test_game.get_patches().count(), 3)
    
    def test_game_functions_get_categories(self):
        print(self.test_game.get_categories())
        self.assertEqual(self.test_game.get_categories().count(), 7)
    
    def test_game_functions_get_latest_patch(self):
        newest_patch = self.test_game.get_patches().latest('creation_date')
        self.assertEqual(self.test_game.get_latest_patch(), newest_patch)

