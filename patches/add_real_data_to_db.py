import datetime
import json
import random
from games.models import Game
from categories.models import Category
from patches.models import Patch, PatchOption
from django.contrib.auth.models import User
from django.db.models import Q

def add_real_games_to_db():
    games_data = [
        {
            'image_mini_ref': '/static/images/pokemon_crystal_mini.png',
            'image_ref': '/static/images/pokemon_crystal_front.png',
            'title': 'Pokémon Crystal',
            'developer': 'Game Freak',
            'best_emulator': 'https://bgb.bircd.org/',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Crystal_Version',
            'release_date': datetime.date(2000,9,28)
        },
        {
            'image_mini_ref': '/static/images/pokemon_yellow_mini.png',
            'image_ref': '/static/images/pokemon_yellow_front.webp',
            'title': 'Pokémon Yellow',
            'developer': 'Game Freak',
            'best_emulator': 'https://bgb.bircd.org/',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Yellow_Version',
            'release_date': datetime.date(1995,9,28)
        },
        {
            'image_mini_ref': '/static/images/pokemon_crystal_mini.png',
            'image_ref': '/static/images/pokemon_crystal_front.png',
            'title': 'Pokémon Crystal Clear',
            'developer': 'Game Freak',
            'best_emulator': 'https://bgb.bircd.org/',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Crystal_Version',
            'release_date': datetime.date(2022,3,16)
        },
        {
            'image_mini_ref': '/static/images/pokemon_yellow_mini.png',
            'image_ref': '/static/images/pokemon_yellow_front.webp',
            'title': 'Pokémon NO-BS Yellow',
            'developer': 'Game Freak',
            'best_emulator': 'https://bgb.bircd.org/',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Yellow_Version',
            'release_date': datetime.date(2021,6,21)
        }
    ]
    
    for game_data in games_data:
        game = Game()
        for key, value in game_data.items():
            setattr(game, key, value)
        game.save()
    
def add_real_categories_to_db():
    category = Category()
    category.image_ref = '/static/images/nuzlocke.png'
    category.name = 'Nuzlocke'
    category.description = """The nuzlocke consists on a series of self-imposed challenges designed to make the game more difficult. The two main rules are:

1. Only the first Pokémon per route shall be captured
2. Any pokemon that faints is considered dead and unusable.

These rules and many other subsets of rules will be implemented within this category."""
    category.base_game = Game.objects.get(title='Pokémon Yellow')
    category.save()
    
    category2 = Category()
    category2.image_ref = '/static/images/nuzlocke.png'
    category2.name = 'Nuzlocke'
    category2.description = """The nuzlocke consists on a series of self-imposed challenges designed to make the game more difficult. The two main rules are:

1. Only the first Pokémon per route shall be captured
2. Any pokemon that faints is considered dead and unusable.

These rules and many other subsets of rules will be implemented within this category."""
    category2.base_game = Game.objects.get(title='Pokémon Crystal')
    category2.save()
    
    category3 = Category()
    category3.image_ref = '/static/images/egglocke.png'
    category3.name = 'Egglocke'
    category3.description = 'This category of nuzlocke swaps any caught encounter with a random egg.'
    category3.parent_category = category2
    category3.base_game = Game.objects.get(title='Pokémon Crystal')
    category3.save()
    
    category4 = Category()
    category4.image_ref = '/static/images/egglocke.png'
    category4.name = 'Egglocke'
    category4.description = 'This category of nuzlocke swaps any caught encounter with a random egg.'
    category4.parent_category = category
    category4.base_game = Game.objects.get(title='Pokémon Yellow')
    category4.save()
    
    category5 = Category()
    category5.image_ref = '/static/images/dice.svg'
    category5.name = 'Randomizer'
    category5.description = 'General category for randomizers.'
    category5.parent_category = None
    category5.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category5.save()
    
    category6 = Category()
    category6.image_ref = '/static/images/dice.svg'
    category6.name = 'Warp Randomizer'
    category6.description = 'Randomizes all warps to random locations, while maintaining logic to be able to complete the game.'
    category6.parent_category = category5
    category6.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category6.save()
    
    category7 = Category()
    category7.image_ref = '/static/images/dice.svg'
    category7.name = 'Item Randomizer'
    category7.description = 'Randomizes all items, while maintaining logic to be able to complete the game.'
    category7.parent_category = category5
    category7.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category7.save()
    
    category8 = Category()
    category8.image_ref = '/static/images/dice.svg'
    category8.name = 'Full Item Randomizer'
    category8.description = 'Randomizes all items, including key items, badges and such, while maintaining logic to be able to complete the game.'
    category8.parent_category = category7
    category8.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category8.save()
    
    category9 = Category()
    category9.image_ref = '/static/images/dice.svg'
    category9.name = 'Randomizer'
    category9.description = 'General category for randomizers.'
    category9.parent_category = None
    category9.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category9.save()
    
    category10 = Category()
    category10.image_ref = '/static/images/dice.svg'
    category10.name = 'Warp Randomizer'
    category10.description = 'Randomizes all warps to random locations, while maintaining logic to be able to complete the game.'
    category10.parent_category = category9
    category10.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category10.save()
    
    category11 = Category()
    category11.image_ref = '/static/images/dice.svg'
    category11.name = 'Item Randomizer'
    category11.description = 'Randomizes all items, while maintaining logic to be able to complete the game.'
    category11.parent_category = category9
    category11.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category11.save()
    
    category12 = Category()
    category12.image_ref = '/static/images/dice.svg'
    category12.name = 'Full Item Randomizer'
    category12.description = 'Randomizes all items, including key items, badges and such, while maintaining logic to be able to complete the game.'
    category12.parent_category = category11
    category12.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category12.save()
    
    category13 = Category()
    category13.image_ref = '/static/images/dice.svg'
    category13.name = 'Randomizer'
    category13.description = 'General category for randomizers.'
    category13.parent_category = None
    category13.base_game = Game.objects.get(title='Pokémon Crystal')
    category13.save()
    
    category14 = Category()
    category14.image_ref = '/static/images/dice.svg'
    category14.name = 'Randomizer'
    category14.description = 'General category for randomizers.'
    category14.parent_category = None
    category14.base_game = Game.objects.get(title='Pokémon Yellow')
    category14.save()
    
def add_real_patch_options_to_db():
    pOption = PatchOption()
    pOption.category = Category.objects.get(name='Nuzlocke', base_game__title='Pokémon Yellow')
    pOption.code_file = 'patches/game_patches/pokemon_yellow_nuzlocke.py'
    pOption.name = 'Pokémon death'
    pOption.description = 'Prevents a pokemon that has fainted from ever reviving.'
    pOption.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption.save()
    
    pOption2 = PatchOption()
    pOption2.category = Category.objects.get(name='Nuzlocke', base_game__title='Pokémon Crystal')
    pOption2.code_file = 'patches/game_patches/pokemon_crystal_nuzlocke.py'
    pOption2.name = 'Pokémon death'
    pOption2.description = 'Prevents a pokemon that has fainted from ever reviving.'
    pOption2.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption2.save()
    
    pOption3 = PatchOption()
    pOption3.category = Category.objects.get(name='Egglocke', base_game__title='Pokémon Yellow')
    pOption3.code_file = 'patches/game_patches/pokemon_yellow_egglocke.py'
    pOption3.name = 'Swap encounter with egg'
    pOption3.description = 'Swaps the caught encounter with a random egg from the active box.'
    pOption3.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption3.save()
    
    pOption4 = PatchOption()
    pOption4.category = Category.objects.get(name='Egglocke', base_game__title='Pokémon Crystal')
    pOption4.code_file = 'patches/game_patches/pokemon_crystal_egglocke.py'
    pOption4.name = 'Swap encounter with egg'
    pOption4.description = 'Swaps the caught encounter with a random egg from the active box.'
    pOption4.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption4.save()
    
    pOption5 = PatchOption()
    pOption5.category = Category.objects.get(name='Randomizer', base_game__title='Pokémon Yellow')
    pOption5.code_file = 'patches/game_patches/pokemon_yellow_wild_randomizer.py'
    pOption5.name = 'Wild encounter randomizer'
    pOption5.description = 'Randomizes the encounters of wild pokemons.'
    pOption5.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption5.save()
    
    pOption6 = PatchOption()
    pOption6.category = Category.objects.get(name='Randomizer', base_game__title='Pokémon Crystal')
    pOption6.code_file = 'patches/game_patches/pokemon_crystal_wild_randomizer.py'
    pOption6.name = 'Wild encounter randomizer'
    pOption6.description = 'Randomizes the encounters of wild pokemons.'
    pOption6.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption6.save()
    
    pOption7 = PatchOption()
    pOption7.category = Category.objects.get(name='Randomizer', base_game__title='Pokémon NO-BS Yellow')
    pOption7.code_file = 'patches/game_patches/pokemon_nobs_yellow_wild_randomizer.py'
    pOption7.name = 'Wild encounter randomizer'
    pOption7.description = 'Randomizes the encounters of wild pokemons.'
    pOption7.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption7.save()
    
    pOption8 = PatchOption()
    pOption8.category = Category.objects.get(name='Randomizer', base_game__title='Pokémon Crystal Clear')
    pOption8.code_file = 'patches/game_patches/pokemon_crystal_clear_wild_randomizer.py'
    pOption8.name = 'Wild encounter randomizer'
    pOption8.description = 'Randomizes the encounters of wild pokemons.'
    pOption8.fields = json.dumps({'fields': {'activated': 'Boolean'}})
    pOption8.save()
    
def add_real_patches_to_db():
    patch = Patch()
    patch.name = 'Basic Nuzlocke'
    patch.downloads = random.randint(0, 1000)
    patch.favorites = random.randint(0, 1000)
    patch.creator = User.objects.get(username='admin')
    patch.creation_date = datetime.date.today()
    patch.field_data = json.dumps({'fields': {'activated': True}})
    patch.save()
    patch.patch_options.set(PatchOption.objects.filter(category__name='Nuzlocke', category__base_game__title='Pokémon Crystal'))
    
    patch2 = Patch()
    patch2.name = 'Basic Egglocke'
    patch2.downloads = random.randint(0, 1000)
    patch2.favorites = random.randint(0, 1000)
    patch2.creator = User.objects.get(username='admin')
    patch2.creation_date = datetime.date.today()
    patch2.parent_patch = patch
    patch2.field_data = json.dumps({'fields': {'activated': True}})
    patch2.save()
    patch2.patch_options.set(PatchOption.objects.filter(category__name='Egglocke', category__base_game__title='Pokémon Crystal'))
    
    patch3 = Patch()
    patch3.name = 'Basic Nuzlocke'
    patch3.downloads = random.randint(0, 1000)
    patch3.favorites = random.randint(0, 1000)
    patch3.creator = User.objects.get(username='admin')
    patch3.creation_date = datetime.date.today()
    patch3.field_data = json.dumps({'fields': {'activated': True}})
    patch3.save()
    patch3.patch_options.set(PatchOption.objects.filter(category__name='Nuzlocke', category__base_game__title='Pokémon Yellow'))
    
    patch4 = Patch()
    patch4.name = 'Basic Egglocke'
    patch4.downloads = random.randint(0, 1000)
    patch4.favorites = random.randint(0, 1000)
    patch4.creator = User.objects.get(username='admin')
    patch4.creation_date = datetime.date.today()
    patch4.parent_patch = patch3
    patch4.field_data = json.dumps({'fields': {'activated': True}})
    patch4.save()
    patch4.patch_options.set(PatchOption.objects.filter(category__name='Egglocke', category__base_game__title='Pokémon Yellow'))
    
    patch5 = Patch()
    patch5.name = 'Wild Pokemon Randomizer'
    patch5.downloads = random.randint(0, 1000)
    patch5.favorites = random.randint(0, 1000)
    patch5.creator = User.objects.get(username='admin')
    patch5.creation_date = datetime.date.today()
    patch5.field_data = json.dumps({'fields': {'activated': True}})
    patch5.save()
    patch5.patch_options.set(PatchOption.objects.filter(category__name='Randomizer', category__base_game__title='Pokémon Crystal'))
    
    patch6 = Patch()
    patch6.name = 'Warp Pokemon Randomizer'
    patch6.downloads = random.randint(0, 1000)
    patch6.favorites = random.randint(0, 1000)
    patch6.creator = User.objects.get(username='admin')
    patch6.creation_date = datetime.date.today()
    patch6.field_data = json.dumps({'fields': {'activated': True}})
    patch6.save()
    patch6.patch_options.set(PatchOption.objects.filter(category__name='Randomizer', category__base_game__title='Pokémon Crystal Clear'))
    
    patch7 = Patch()
    patch7.name = 'Warp Pokemon Randomizer'
    patch7.downloads = random.randint(0, 1000)
    patch7.favorites = random.randint(0, 1000)
    patch7.creator = User.objects.get(username='admin')
    patch7.creation_date = datetime.date.today()
    patch7.field_data = json.dumps({'fields': {'activated': True}})
    patch7.save()
    patch7.patch_options.set(PatchOption.objects.filter(category__name='Randomizer', category__base_game__title='Pokémon NO-BS Yellow'))
    
    patch8 = Patch()
    patch8.name = 'Wild Pokemon Randomizer Nuzlocke'
    patch8.downloads = random.randint(0, 1000)
    patch8.favorites = random.randint(0, 1000)
    patch8.creator = User.objects.get(username='admin')
    patch8.creation_date = datetime.date.today()
    patch8.parent_patch = patch3
    patch8.field_data = json.dumps({'fields': {'activated': True}})
    patch8.save()
    pos = PatchOption.objects.filter(
        Q(category__name='Randomizer', category__base_game__title='Pokémon Yellow') |
        Q(category__name='Nuzlocke', category__base_game__title='Pokémon Yellow')
    )
    patch8.patch_options.set(pos)
    