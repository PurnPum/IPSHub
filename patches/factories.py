import random
import factory
from django.contrib.auth.models import User
from .models import *
from categories.factories import CategoryFactory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')

class PatchOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatchOption

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    #github_issue = factory.Faker('url')

class PatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patch

    name = factory.Faker('word')
    downloads = factory.Faker('random_int', min=0, max=1000)
    favorites = factory.Faker('random_int', min=0, max=1000)
    creation_date = factory.Faker('date')
    creator = factory.SubFactory(UserFactory)
    patch_options = factory.SubFactory(PatchOptionFactory, _quantity=random.randint(1, 3))
    download_link = factory.Faker('url')
    patch_hash = factory.Faker('word')

    @factory.post_generation
    def patch_options(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for patch_option in extracted:
                self.patch_options.add(patch_option)
        else:
            # Create a random number of PatchOptions and associate with this Patch
            for _ in range(random.randint(1, 3)):
                self.patch_options.add(PatchOptionFactory())

class POFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = POField

    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    field_type = factory.Faker('word')
    initial_data = factory.Faker('json')
    
    @factory.lazy_attribute
    def parent_field(self):
        if not hasattr(self, '_depth'):
            self._depth = 0

        if self._depth < 3:  # Control the maximum depth of categories to avoid infinite recursion
            self._depth += 1
            return PatchFactory(_depth=self._depth)
        else:
            return None


class PatchDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatchData

    patch = factory.SubFactory(PatchFactory)
    field = factory.SubFactory(POFieldFactory)
    data = factory.Faker('json')


class DiffFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DiffFile

    filename = factory.Faker('file_name')
    original_file = factory.Faker('file_name')
    trigger_value = factory.Faker('word')
    field = factory.SubFactory(POFieldFactory)


class PatchCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatchComment

    patch = factory.SubFactory(PatchFactory)
    author = factory.SubFactory(UserFactory)
    created = factory.Faker('date')
    comment = factory.Faker('paragraph')


class PatchCommentLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatchCommentLike

    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(PatchCommentFactory)
    likeordislike = factory.Faker('pybool')


class PatchFavFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatchFav

    patch = factory.SubFactory(PatchFactory)
    user = factory.SubFactory(UserFactory)
