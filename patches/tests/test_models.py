from django.contrib.auth.models import User
from django.test import TestCase
from patches.models import Patch, PatchOption
from django.forms import ValidationError
from categories.models import Category
from core.utils import add_data_to_bd

class PatchTestCase(TestCase):
    
    def setUp(self):
        add_data_to_bd()
        self.test_patch = Patch.objects.get(name='Basic Egglocke Crystal')
        self.test_patch2 = Patch.objects.get(name='Basic Nuzlocke Yellow')
        self.test_po1 = PatchOption.objects.get(name='Pokémon death Yellow')
        self.test_po2 = PatchOption.objects.get(name='Pokémon death Crystal')
        
    def test_str(self):
        self.setUp()
        self.assertEqual(str(self.test_patch), 'Basic Egglocke Crystal')
        
    def test_clean(self):
        self.setUp()
        self.test_patch.clean()
        self.test_patch2.clean()
        
        self.test_patch.parent_patch = self.test_patch
        with self.assertRaises(ValidationError):
            self.test_patch.clean()
        
        self.setUp()
        
        self.test_patch2.parent_patch = Patch.objects.get(name='Wild Pokemon Randomizer Nuzlocke Yellow')
        with self.assertRaises(ValidationError):
            self.test_patch2.clean()
            
        self.setUp()
            
        self.test_patch.patch_options.set([self.test_po1, self.test_po2])
        with self.assertRaises(ValidationError):
            self.test_patch.clean()
            
        self.setUp()
        
        self.test_patch.name = 'Basic Nuzlocke Crystal'
        with self.assertRaises(ValidationError):
            self.test_patch.clean()
            
        