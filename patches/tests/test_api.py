from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse

from games.models import Game
from core.add_real_data_to_db import add_data_to_bd

class APITest(TestCase):
    
    def setUp(self):
        add_data_to_bd()
        print("Finished setting up the db!")
        
    def test_patches_main(self):
        url = reverse('patches')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        
        self.assertIn('<div id="active_modal" class="modal fade" tabindex="-1" aria-labelledby="active_modal_title" aria-hidden="true">', response.content.decode('utf-8'))

    def test_games_main(self):
        url = reverse('games')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertIn('<div id="active_modal" class="modal fade" tabindex="-1" aria-labelledby="active_modal_title" aria-hidden="true">', response.content.decode('utf-8'))
        
    def test_patchgen_main(self):
        url = reverse('patch_generator')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertIn('<div hx-swap-oob="true" id="games-main-layout" class="accordion accordion-flush row d-flex custom-bottom-border pb-2"', response.content.decode('utf-8'))
        
    def test_patchgen_game(self):
        url = reverse('patch_generator')
        game = Game.objects.order_by('?').first().id
        response = self.client.get(f"{url}?selectedGame={game}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertIn('<h3 id="nav-title" class="fw-bold flex-grow-1 d-flex align-items-center my-2 h2 justify-content-center">Patch Generator</h3>', response.content.decode('utf-8'))

