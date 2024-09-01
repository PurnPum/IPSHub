from django.forms import ValidationError
from django.test import TestCase
from categories.models import Category
from core.utils import add_data_to_bd

class CategoryTestCase(TestCase):

    def setUp(self):
        add_data_to_bd()
        self.test_category = Category.objects.get(name='Egglocke Yellow')
        self.test_category2 = Category.objects.get(name='Super Wedlocke Yellow')
    
    def test_str(self):
        self.setUp()
        self.assertEqual(str(self.test_category), 'Egglocke Yellow')
        
    def test_clean(self):
        
        self.setUp()
        self.test_category.clean()
        
        self.test_category.parent_category = self.test_category
        with self.assertRaises(ValidationError):
            self.test_category.clean()
        
        self.setUp()
        
        self.test_category.parent_category = Category.objects.get(name='Special Egglocke Yellow')
        with self.assertRaises(ValidationError):
            self.test_category.clean()
            
        self.setUp()
            
        self.test_category.parent_category = Category.objects.get(name='Egglocke Crystal')
        with self.assertRaises(ValidationError):
            self.test_category.clean()
            
        self.setUp()
    
    def test_get_all_parents(self):
        self.setUp()
        self.assertEqual(self.test_category.get_all_parents(), [Category.objects.get(name='Nuzlocke Yellow')])
        
    def test_get_all_children(self):
        self.setUp()
        self.assertEqual(self.test_category.get_all_children(), [Category.objects.get(name='Special Egglocke Yellow')])
        
    def test_get_main_parent(self):
        self.setUp()
        self.assertEqual(self.test_category.get_main_parent(), Category.objects.get(name='Nuzlocke Yellow'))