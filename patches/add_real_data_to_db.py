import datetime
import json
import random
from games.models import Game
from categories.models import Category
from patches.models import Patch, PatchOption, POField, PatchData, DiffFile
from django.contrib.auth.models import User
from django.db.models import Q

def clean_db():
    Game.objects.all().delete()
    Patch.objects.all().delete()
    PatchOption.objects.all().delete()
    Category.objects.all().delete()
    POField.objects.all().delete()
    PatchData.objects.all().delete()

def add_real_games_to_db():
    games_data = [
        {
            'image_mini_ref': '/static/images/pokemon_crystal_mini.png',
            'image_ref': '/static/images/pokemon_crystal_front.png',
            'title': 'Pokémon Crystal',
            'developer': 'Game Freak',
            'best_emulator': 'BGB',
            'best_emulator_url': 'https://bgb.bircd.org/',
            'type': 'Vanilla Game',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Crystal_Version',
            'release_date': datetime.date(2000,9,28),
            'repository': 'https://github.com/pret/pokecrystal.git',
            'patch_file_name': 'pokecrystal.gbc',
            'patch_sha': 'f2f52230b536214ef7c9924f483392993e226cfb'
        },
        {
            'image_mini_ref': '/static/images/pokemon_yellow_mini.png',
            'image_ref': '/static/images/pokemon_yellow_front.webp',
            'title': 'Pokémon Yellow',
            'developer': 'Game Freak',
            'best_emulator': 'BGB',
            'best_emulator_url': 'https://bgb.bircd.org/',
            'type': 'Vanilla Game',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Yellow_Version',
            'release_date': datetime.date(1995,9,28),
            'repository': 'https://github.com/pret/pokeyellow.git',
            'patch_file_name': 'pokeyellow.gbc',
            'patch_sha': 'cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1'
        },
        {
            'image_mini_ref': '/static/images/pokemon_crystal_mini.png',
            'image_ref': '/static/images/pokemon_crystal_front.png',
            'title': 'Pokémon Crystal Clear',
            'developer': 'ShockSlayer',
            'best_emulator': 'Gambatte',
            'best_emulator_url': 'https://github.com/pokemon-speedrunning/gambatte-speedrun',
            'type': 'ROM Hack',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Crystal_Version',
            'release_date': datetime.date(2022,3,16),
            'repository': 'https://github.com/pret/pokecrystal.git',
            'patch_file_name': 'pokecrystal.gbc',
            'patch_sha': 'f2f52230b536214ef7c9924f483392993e226cfb'
        },
        {
            'image_mini_ref': '/static/images/pokemon_yellow_mini.png',
            'image_ref': '/static/images/pokemon_yellow_front.webp',
            'title': 'Pokémon NO-BS Yellow',
            'developer': 'Game Freak',
            'best_emulator': 'Gambatte',
            'best_emulator_url': 'https://github.com/pokemon-speedrunning/gambatte-speedrun',
            'type': 'ROM Hack',
            'extra_info': 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Yellow_Version',
            'release_date': datetime.date(2021,6,21),
            'repository': 'https://github.com/pret/pokeyellow.git',
            'patch_file_name': 'pokeyellow.gbc',
            'patch_sha': 'cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1'
        }
    ]
    
    for game_data in games_data:
        game = Game()
        for key, value in game_data.items():
            setattr(game, key, value)
        game.save()
    
def add_real_categories_to_db():
    category = Category()
    category.image_ref = '/static/images/nuzlocke.jpg'
    category.name = 'Nuzlocke Yellow'
    category.description = """The nuzlocke consists on a series of self-imposed challenges designed to make the game more difficult. The two main rules are:

1. Only the first Pokémon per route shall be captured
2. Any pokemon that faints is considered dead and unusable.

These rules and many other subsets of rules will be implemented within this category."""
    category.base_game = Game.objects.get(title='Pokémon Yellow')
    category.save()
    
    category2 = Category()
    category2.image_ref = '/static/images/nuzlocke.jpg'
    category2.name = 'Nuzlocke Crystal'
    category2.description = """The nuzlocke consists on a series of self-imposed challenges designed to make the game more difficult. The two main rules are:

1. Only the first Pokémon per route shall be captured
2. Any pokemon that faints is considered dead and unusable.

These rules and many other subsets of rules will be implemented within this category."""
    category2.base_game = Game.objects.get(title='Pokémon Crystal')
    category2.save()
    
    category3 = Category()
    category3.image_ref = '/static/images/egglocke.png'
    category3.name = 'Egglocke Crystal'
    category3.description = 'This category of nuzlocke swaps any caught encounter with a random egg.'
    category3.parent_category = category2
    category3.base_game = Game.objects.get(title='Pokémon Crystal')
    category3.save()
    
    category4 = Category()
    category4.image_ref = '/static/images/egglocke.png'
    category4.name = 'Egglocke Yellow'
    category4.description = 'This category of nuzlocke swaps any caught encounter with a random egg.'
    category4.parent_category = category
    category4.base_game = Game.objects.get(title='Pokémon Yellow')
    category4.save()
    
    category5 = Category()
    category5.image_ref = '/static/images/dice.svg'
    category5.name = 'Randomizer Crystal Clear'
    category5.description = 'General category for randomizers.'
    category5.parent_category = None
    category5.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category5.save()
    
    category6 = Category()
    category6.image_ref = '/static/images/dice.svg'
    category6.name = 'Warp Randomizer Crystal Clear'
    category6.description = 'Randomizes all warps to random locations, while maintaining logic to be able to complete the game.'
    category6.parent_category = category5
    category6.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category6.save()
    
    category7 = Category()
    category7.image_ref = '/static/images/dice.svg'
    category7.name = 'Item Randomizer Crystal Clear'
    category7.description = 'Randomizes all items, while maintaining logic to be able to complete the game.'
    category7.parent_category = category5
    category7.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category7.save()
    
    category8 = Category()
    category8.image_ref = '/static/images/dice.svg'
    category8.name = 'Full Item Randomizer Crystal Clear'
    category8.description = 'Randomizes all items, including key items, badges and such, while maintaining logic to be able to complete the game.'
    category8.parent_category = category7
    category8.base_game = Game.objects.get(title='Pokémon Crystal Clear')
    category8.save()
    
    category9 = Category()
    category9.image_ref = '/static/images/dice.svg'
    category9.name = 'Randomizer NO-BS Yellow'
    category9.description = 'General category for randomizers.'
    category9.parent_category = None
    category9.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category9.save()
    
    category10 = Category()
    category10.image_ref = '/static/images/dice.svg'
    category10.name = 'Warp Randomizer NO-BS Yellow'
    category10.description = 'Randomizes all warps to random locations, while maintaining logic to be able to complete the game.'
    category10.parent_category = category9
    category10.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category10.save()
    
    category11 = Category()
    category11.image_ref = '/static/images/dice.svg'
    category11.name = 'Item Randomizer NO-BS Yellow'
    category11.description = 'Randomizes all items, while maintaining logic to be able to complete the game.'
    category11.parent_category = category9
    category11.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category11.save()
    
    category12 = Category()
    category12.image_ref = '/static/images/dice.svg'
    category12.name = 'Full Item Randomizer NO-BS Yellow'
    category12.description = 'Randomizes all items, including key items, badges and such, while maintaining logic to be able to complete the game.'
    category12.parent_category = category11
    category12.base_game = Game.objects.get(title='Pokémon NO-BS Yellow')
    category12.save()
    
    category13 = Category()
    category13.image_ref = '/static/images/dice.svg'
    category13.name = 'Randomizer Crystal'
    category13.description = 'General category for randomizers.'
    category13.parent_category = None
    category13.base_game = Game.objects.get(title='Pokémon Crystal')
    category13.save()
    
    category14 = Category()
    category14.image_ref = '/static/images/dice.svg'
    category14.name = 'Randomizer Yellow'
    category14.description = 'General category for randomizers.'
    category14.parent_category = None
    category14.base_game = Game.objects.get(title='Pokémon Yellow')
    category14.save()
    
    category15 = Category()
    category15.image_ref = '/static/images/wedlocke.svg'
    category15.name = 'Wedlocke Yellow'
    category15.description = 'This category of nuzlocke links 2 encounters and if one dies so does the other.'
    category15.parent_category = category
    category15.base_game = Game.objects.get(title='Pokémon Yellow')
    category15.save()
    
    category16 = Category()
    category16.image_ref = '/static/images/egglocke.png'
    category16.name = 'Special Egglocke Yellow'
    category16.description = 'This category of nuzlocke swaps any caught encounter with a random egg.'
    category16.parent_category = category4
    category16.base_game = Game.objects.get(title='Pokémon Yellow')
    category16.save()
    
    category16 = Category()
    category16.image_ref = '/static/images/wedlocke.svg'
    category16.name = 'Super Wedlocke Yellow'
    category16.description = 'This category of wedlocke creates an entire family tree instead of just pairs.'
    category16.parent_category = category15
    category16.base_game = Game.objects.get(title='Pokémon Yellow')
    category16.save()
    
    category17 = Category()
    category17.image_ref = '/static/images/other.webp'
    category17.name = 'Translated yellow text to Spanish'
    category17.description = 'Translates part of the game into Spanish.'
    category17.parent_category = None
    category17.base_game = Game.objects.get(title='Pokémon Yellow')
    category17.save()
    
    category18 = Category()
    category18.image_ref = '/static/images/other.webp'
    category18.name = 'Translated crystal text to Spanish'
    category18.description = 'Translates part of the game into Spanish.'
    category18.parent_category = None
    category18.base_game = Game.objects.get(title='Pokémon Crystal')
    category18.save()
    
def add_real_patch_options_to_db():
    pOption = PatchOption()
    pOption.category = Category.objects.get(name='Nuzlocke Yellow', base_game__title='Pokémon Yellow')
    pOption.name = 'Pokémon death Yellow'
    pOption.description = 'Prevents a pokemon that has fainted from ever reviving.'
    pOption.save()
    
    pOption2 = PatchOption()
    pOption2.category = Category.objects.get(name='Nuzlocke Crystal', base_game__title='Pokémon Crystal')
    pOption2.name = 'Pokémon death Crystal'
    pOption2.description = 'Prevents a pokemon that has fainted from ever reviving.'
    pOption2.save()
    
    pOption3 = PatchOption()
    pOption3.category = Category.objects.get(name='Egglocke Yellow', base_game__title='Pokémon Yellow')
    pOption3.name = 'Swap encounter with egg Yellow'
    pOption3.description = 'Swaps the caught encounter with a random egg from the active box.'
    pOption3.save()
    
    pOption4 = PatchOption()
    pOption4.category = Category.objects.get(name='Egglocke Crystal', base_game__title='Pokémon Crystal')
    pOption4.name = 'Swap encounter with egg Crystal'
    pOption4.description = 'Swaps the caught encounter with a random egg from the active box.'
    pOption4.save()
    
    pOption5 = PatchOption()
    pOption5.category = Category.objects.get(name='Randomizer Yellow', base_game__title='Pokémon Yellow')
    pOption5.name = 'Wild encounter randomizer Yellow'
    pOption5.description = 'Randomizes the encounters of wild pokemons.'
    pOption5.save()
    
    pOption6 = PatchOption()
    pOption6.category = Category.objects.get(name='Randomizer Crystal', base_game__title='Pokémon Crystal')
    pOption6.name = 'Wild encounter randomizer Crystal'
    pOption6.description = 'Randomizes the encounters of wild pokemons.'
    pOption6.save()
    
    pOption7 = PatchOption()
    pOption7.category = Category.objects.get(name='Randomizer NO-BS Yellow', base_game__title='Pokémon NO-BS Yellow')
    pOption7.name = 'Wild encounter randomizer NO-BS Yellow'
    pOption7.description = 'Randomizes the encounters of wild pokemons.'
    pOption7.save()
    
    pOption8 = PatchOption()
    pOption8.category = Category.objects.get(name='Randomizer Crystal Clear', base_game__title='Pokémon Crystal Clear')
    pOption8.name = 'Wild encounter randomizer Crystal Clear'
    pOption8.description = 'Randomizes the encounters of wild pokemons.'
    pOption8.save()
    
    pOption9 = PatchOption()
    pOption9.category = Category.objects.get(name='Wedlocke Yellow', base_game__title='Pokémon Yellow')
    pOption9.name = 'Kill the partner of the fainted Pokemon'
    pOption9.description = 'Once a pokemon dies, also kill the partner they had been linked with.'
    pOption9.save()
    
    pOption10 = PatchOption()
    pOption10.category = Category.objects.get(name='Wedlocke Yellow', base_game__title='Pokémon Yellow')
    pOption10.name = 'Link the latest caught pokemon'
    pOption10.description = 'After capturing a Pokemon, link it with a partner of a different gender that does not have a partner.'
    pOption10.save()
    
    pOption11 = PatchOption()
    pOption11.category = Category.objects.get(name='Super Wedlocke Yellow', base_game__title='Pokémon Yellow')
    pOption11.name = 'Add the latest caught pokemon to the family tree'
    pOption11.description = 'After capturing a Pokemon, add it to the family tree depending on who helped catch it.'
    pOption11.save()
    
    pOption11 = PatchOption()
    pOption11.category = Category.objects.get(name='Special Egglocke Yellow', base_game__title='Pokémon Yellow')
    pOption11.name = 'Special egglocke'
    pOption11.description = 'This is a special egglocke template.'
    pOption11.save()
    
    pOption12 = PatchOption()
    pOption12.category = Category.objects.get(name='Translated yellow text to Spanish', base_game__title='Pokémon Yellow')
    pOption12.name = 'Translated yellow text to Spanish'
    pOption12.description = 'Translates the text to Spanish.'
    pOption12.save()
    
    pOption13 = PatchOption()
    pOption13.category = Category.objects.get(name='Translated crystal text to Spanish', base_game__title='Pokémon Crystal')
    pOption13.name = 'Translated crystal text to Spanish'
    pOption13.description = 'Translates the text to Spanish.'
    pOption13.save()
    
def add_real_fields_to_db():
    
    field = POField()
    field.name = 'Binary selector'
    field.description = 'Selection between true and false'
    field.field_type = 'Boolean'
    field.initial_data = json.dumps({'data': ["True", "False"]})
    field.parent_field = None
    field.default_data = json.dumps({'data': "False"})
    field.patch_option = PatchOption.objects.get(name='Pokémon death Yellow')
    field.save()
    
    field2 = POField()
    field2.name = 'Binary selector'
    field2.description = 'Selection between true and false'
    field2.field_type = 'Boolean'
    field2.initial_data = json.dumps({'data': ["True", "False"]})
    field2.parent_field = None
    field2.default_data = json.dumps({'data': "False"})
    field2.patch_option = PatchOption.objects.get(name='Pokémon death Crystal')
    field2.save()
    
    field3 = POField()
    field3.name = 'Binary selector'
    field3.description = 'Selection between true and false'
    field3.field_type = 'Boolean'
    field3.initial_data = json.dumps({'data': ["True", "False"]})
    field3.parent_field = None
    field3.default_data = json.dumps({'data': "False"})
    field3.patch_option = PatchOption.objects.get(name='Swap encounter with egg Yellow')
    field3.save()
    
    field4 = POField()
    field4.name = 'Binary selector'
    field4.description = 'Selection between true and false'
    field4.field_type = 'Boolean'
    field4.initial_data = json.dumps({'data': ["True", "False"]})
    field4.parent_field = None
    field4.default_data = json.dumps({'data': "False"})
    field4.patch_option = PatchOption.objects.get(name='Add the latest caught pokemon to the family tree')
    field4.save()
    
    field5 = POField()
    field5.name = 'Binary selector'
    field5.description = 'Selection between true and false'
    field5.field_type = 'Boolean'
    field5.initial_data = json.dumps({'data': ["True", "False"]})
    field5.parent_field = None
    field5.default_data = json.dumps({'data': "False"})
    field5.patch_option = PatchOption.objects.get(name='Wild encounter randomizer Crystal')
    field5.save()
    
    field6 = POField()
    field6.name = 'Binary selector'
    field6.description = 'Selection between true and false'
    field6.field_type = 'Boolean'
    field6.initial_data = json.dumps({'data': ["True", "False"]})
    field6.parent_field = None
    field6.default_data = json.dumps({'data': "False"})
    field6.patch_option = PatchOption.objects.get(name='Kill the partner of the fainted Pokemon')
    field6.save()
    
    field7 = POField()
    field7.name = 'Binary selector'
    field7.description = 'Selection between true and false'
    field7.field_type = 'Boolean'
    field7.initial_data = json.dumps({'data': ["True", "False"]})
    field7.parent_field = None
    field7.default_data = json.dumps({'data': "False"})
    field7.patch_option = PatchOption.objects.get(name='Swap encounter with egg Crystal')
    field7.save()
    
    field8 = POField()
    field8.name = 'Binary selector'
    field8.description = 'Selection between true and false'
    field8.field_type = 'Boolean'
    field8.initial_data = json.dumps({'data': ["True", "False"]})
    field8.parent_field = None
    field8.default_data = json.dumps({'data': "False"})
    field8.patch_option = PatchOption.objects.get(name='Wild encounter randomizer NO-BS Yellow')
    field8.save()
    
    field9 = POField()
    field9.name = 'Binary selector'
    field9.description = 'Selection between true and false'
    field9.field_type = 'Boolean'
    field9.initial_data = json.dumps({'data': ["True", "False"]})
    field9.parent_field = None
    field9.default_data = json.dumps({'data': "False"})
    field9.patch_option = PatchOption.objects.get(name='Special egglocke')
    field9.save()
    
    field10 = POField()
    field10.name = 'Binary selector'
    field10.description = 'Selection between true and false'
    field10.field_type = 'Boolean'
    field10.initial_data = json.dumps({'data': ["True", "False"]})
    field10.parent_field = None
    field10.default_data = json.dumps({'data': "False"})
    field10.patch_option = PatchOption.objects.get(name='Wild encounter randomizer Crystal Clear')
    field10.save()
    
    field11 = POField()
    field11.name = 'Binary selector'
    field11.description = 'Selection between true and false'
    field11.field_type = 'Boolean'
    field11.initial_data = json.dumps({'data': ["True", "False"]})
    field11.parent_field = None
    field11.default_data = json.dumps({'data': "False"})
    field11.patch_option = PatchOption.objects.get(name='Wild encounter randomizer Yellow')
    field11.save()
    
    field12 = POField()
    field12.name = 'Binary selector'
    field12.description = 'Selection between true and false'
    field12.field_type = 'Boolean'
    field12.initial_data = json.dumps({'data': ["True", "False"]})
    field12.parent_field = None
    field12.default_data = json.dumps({'data': "False"})
    field12.patch_option = PatchOption.objects.get(name='Link the latest caught pokemon')
    field12.save()
    
    field13 = POField()
    field13.name = 'Multiple choice'
    field13.description = 'Selection between multiple choices'
    field13.field_type = 'Text'
    field13.initial_data = json.dumps({'data': ["Option1", "Opcion2", "Opcion3"]})
    field13.parent_field = None
    field13.default_data = json.dumps({'data': "Opcion2"})
    field13.patch_option = PatchOption.objects.get(name='Link the latest caught pokemon')
    field13.save()
    
    field14 = POField()
    field14.name = 'Text input'
    field14.description = 'Input a text'
    field14.field_type = 'Text'
    field14.initial_data = json.dumps({'data': ""})
    field14.parent_field = None
    field14.default_data = json.dumps({'data': ""})
    field14.patch_option = PatchOption.objects.get(name='Kill the partner of the fainted Pokemon')
    field14.save()
    
    field15 = POField()
    field15.name = 'Translate yellow main menu'
    field15.description = 'Translates the Continue/New Game menu'
    field15.field_type = 'Boolean'
    field15.initial_data = json.dumps({'data': ["True", "False"]})
    field15.parent_field = None
    field15.default_data = json.dumps({'data': "False"})
    field15.patch_option = PatchOption.objects.get(name='Translated yellow text to Spanish')
    field15.save()
    
    field15 = POField()
    field15.name = 'Translate crystal main menu'
    field15.description = 'Translates the Continue/New Game menu'
    field15.field_type = 'Boolean'
    field15.initial_data = json.dumps({'data': ["True", "False"]})
    field15.parent_field = None
    field15.default_data = json.dumps({'data': "False"})
    field15.patch_option = PatchOption.objects.get(name='Translated crystal text to Spanish')
    field15.save()
    
def add_real_patches_to_db():
    patch = Patch()
    patch.name = 'Basic Nuzlocke Crystal'
    patch.downloads = random.randint(0, 1000)
    patch.favorites = random.randint(0, 1000)
    patch.creator = User.objects.get(username='admin')
    patch.creation_date = datetime.date.today()
    patch.download_link = 'static/patches/PokemonCrystal/patch.ips'
    patch.save()
    patch.patch_options.set(PatchOption.objects.filter(category__name='Nuzlocke Crystal', category__base_game__title='Pokémon Crystal'))
    add_real_patch_data_to_db(patch)
    patch.save()
    
    patch2 = Patch()
    patch2.name = 'Basic Egglocke Crystal'
    patch2.downloads = random.randint(0, 1000)
    patch2.favorites = random.randint(0, 1000)
    patch2.creator = User.objects.get(username='admin')
    patch2.creation_date = datetime.date.today()
    patch2.parent_patch = patch
    patch2.download_link = 'static/patches/PokemonCrystal/patch.ips'
    patch2.save()
    patch2.patch_options.set(PatchOption.objects.filter(category__name='Egglocke Crystal', category__base_game__title='Pokémon Crystal'))
    add_real_patch_data_to_db(patch2)
    patch2.save()
    
    patch3 = Patch()
    patch3.name = 'Basic Nuzlocke Yellow'
    patch3.downloads = random.randint(0, 1000)
    patch3.favorites = random.randint(0, 1000)
    patch3.creator = User.objects.get(username='admin')
    patch3.creation_date = datetime.date.today()
    patch3.download_link = 'static/patches/PokemonYellow/patch.ips'
    patch3.save()
    patch3.patch_options.set(PatchOption.objects.filter(category__name='Nuzlocke Yellow', category__base_game__title='Pokémon Yellow'))
    add_real_patch_data_to_db(patch3)
    patch3.save()
    
    patch4 = Patch()
    patch4.name = 'Basic Egglocke Yellow'
    patch4.downloads = random.randint(0, 1000)
    patch4.favorites = random.randint(0, 1000)
    patch4.creator = User.objects.get(username='admin')
    patch4.creation_date = datetime.date.today()
    patch4.parent_patch = patch3
    patch4.download_link = 'static/patches/PokemonYellow/patch.ips'
    patch4.save()
    patch4.patch_options.set(PatchOption.objects.filter(category__name='Egglocke Yellow', category__base_game__title='Pokémon Yellow'))
    add_real_patch_data_to_db(patch4)
    patch4.save()
    
    patch5 = Patch()
    patch5.name = 'Wild Pokemon Randomizer Crystal'
    patch5.downloads = random.randint(0, 1000)
    patch5.favorites = random.randint(0, 1000)
    patch5.creator = User.objects.get(username='admin')
    patch5.creation_date = datetime.date.today()
    patch5.download_link = 'static/patches/PokemonCrystal/patch.ips'
    patch5.save()
    patch5.patch_options.set(PatchOption.objects.filter(category__name='Randomizer Crystal', category__base_game__title='Pokémon Crystal'))
    add_real_patch_data_to_db(patch5)
    patch5.save()
    
    patch6 = Patch()
    patch6.name = 'Warp Pokemon Randomizer Crystal Clear'
    patch6.downloads = random.randint(0, 1000)
    patch6.favorites = random.randint(0, 1000)
    patch6.creator = User.objects.get(username='admin')
    patch6.creation_date = datetime.date.today()
    patch6.download_link = 'static/patches/PokemonCrystalClear/patch.ips'
    patch6.save()
    patch6.patch_options.set(PatchOption.objects.filter(category__name='Randomizer Crystal Clear', category__base_game__title='Pokémon Crystal Clear'))
    add_real_patch_data_to_db(patch6)
    patch6.save()
    
    patch7 = Patch()
    patch7.name = 'Warp Pokemon Randomizer NO-BS Yellow'
    patch7.downloads = random.randint(0, 1000)
    patch7.favorites = random.randint(0, 1000)
    patch7.creator = User.objects.get(username='admin')
    patch7.creation_date = datetime.date.today()
    patch7.download_link = 'static/patches/PokemonNOBSYellow/patch.ips'
    patch7.save()
    patch7.patch_options.set(PatchOption.objects.filter(category__name='Randomizer NO-BS Yellow', category__base_game__title='Pokémon NO-BS Yellow'))
    add_real_patch_data_to_db(patch7)
    patch7.save()
    
    patch8 = Patch()
    patch8.name = 'Wild Pokemon Randomizer Nuzlocke Yellow'
    patch8.downloads = random.randint(0, 1000)
    patch8.favorites = random.randint(0, 1000)
    patch8.creator = User.objects.get(username='admin')
    patch8.creation_date = datetime.date.today()
    patch8.parent_patch = patch3
    patch8.download_link = 'static/patches/PokemonYellow/patch.ips'
    patch8.save()
    pos = PatchOption.objects.filter(
        Q(category__name='Randomizer Yellow', category__base_game__title='Pokémon Yellow') |
        Q(category__name='Nuzlocke Yellow', category__base_game__title='Pokémon Yellow')
    )
    patch8.patch_options.set(pos)
    add_real_patch_data_to_db(patch8)
    patch8.save()
    
def add_real_diff_files_to_db():
    dfile = DiffFile()
    dfile.filename = 'pokeyellow/engine/menus/main_menu.patch'
    dfile.original_file = 'engine/menus/main_menu.asm'
    dfile.trigger_value = 'True'
    dfile.field = POField.objects.get(name='Translate yellow main menu')
    dfile.save()
    
    dfile2 = DiffFile()
    dfile2.filename = 'pokecrystal/engine/menus/main_menu.patch'
    dfile2.original_file = 'engine/menus/main_menu.asm'
    dfile2.trigger_value = 'True'
    dfile2.field = POField.objects.get(name='Translate crystal main menu')
    dfile2.save()
    
def add_real_patch_data_to_db(patch):
    for po in patch.patch_options.all():
        for field in POField.objects.filter(patch_option=po):
            patchData = PatchData()
            patchData.patch = patch
            patchData.field = field
            patchData.data = 'True'
            patchData.save()
                
def add_anonymous_user_to_db():
    if not User.objects.filter(username='anonymous').exists():
        user = User.objects.create_user(
        username='anonymous', 
        email='anonymous@email.com', 
        password='anon'
        )
        user.save()