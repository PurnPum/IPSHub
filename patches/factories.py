import factory
from django.contrib.auth.models import User
from .models import Patch, PatchOption
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
    code_file = factory.Faker('url')
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

    @factory.post_generation
    def patch_options(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for patch_option in extracted:
                self.patch_options.add(patch_option)
