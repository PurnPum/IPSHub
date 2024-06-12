from django.contrib.auth.models import User

from django.test import TransactionTestCase
from .models import Patch, PatchOption
from .factories import PatchFactory, PatchOptionFactory, UserFactory

class PatchTestCase(TransactionTestCase):

    def setUp(self):
        self.user = UserFactory()
        self.patch_option1 = PatchOptionFactory()
        self.patch_option2 = PatchOptionFactory()
        self.patch = PatchFactory(creator=self.user, patch_options=[self.patch_option1, self.patch_option2])

    def test_patch_creation(self):
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(self.patch.patch_options.count(), 2)
        self.assertEqual(self.patch.creator, self.user)

    def test_patch_options(self):
        patch_options = self.patch.patch_options.all()
        self.assertIn(self.patch_option1, patch_options)
        self.assertIn(self.patch_option2, patch_options)


    #def tearDown(self):
    #    Patch.objects.all().delete()
    #    PatchOption.objects.all().delete()