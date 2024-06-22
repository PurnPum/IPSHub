import datetime
import random
import secrets
from games.models import Game
from categories.models import Category
from patches.models import Patch, PatchOption
from django.contrib.auth.models import User

def clean_db():
    Game.objects.all().delete()
    Patch.objects.all().delete()
    PatchOption.objects.all().delete()
    Category.objects.all().delete()
    
def add_junk_games_to_db():
    game_junk_data = {
        'known_games' : ['Pokemon Yellow', 'Pokemon Gold', 'Pokemon Silver', 'Pokemon Crystal', 'Super Mario Bros', 'The Legend of Zelda', 'Super Metroid', 'Star Fox', 'Final Fantasy 7', 'The Legend of Zelda: A Link to the Past'],
        'release_dates' : ['1999-10-27', '1999-09-29', '1999-09-29', '1998-10-11', '1995-09-28', '1986-09-23', '1996-10-30', '1993-10-28', '1997-11-20', '1990-11-23'],
        'game_developers' : ['Game Freak', 'Game Freak', 'Game Freak', 'Game Freak', 'Nintendo', 'Nintendo', 'Nintendo', 'Nintendo', 'Square (Eidos UK)', 'Nintendo'],
        'emulator_links' : ['https://desmume.org/', 'https://desmume.org/', 'https://desmume.org/', 'https://desmume.org/', 'https://www.mojang.com/2011/12/minecraft-now-available-on-nintendo-3ds-nintendo-ds-and-pc/', 'https://www.mojang.com/2011/12/minecraft-now-available-on-nintendo-3ds-nintendo-ds-and-pc/', 'https://www.mojang.com/2011/12/minecraft-now-available-on-nintendo-3ds-nintendo-ds-and-pc/', 'https://www.mojang.com/2011/12/minecraft-now-available-on-nintendo-3ds-nintendo-ds-and-pc/', 'https://www.mojang.com/2011/12/minecraft-now-available-on-nintendo-3ds-nintendo-ds-and-pc/', 'https://www.mojang.com/2011/12/minecraft-now-available-on-nintendo-3ds-nintendo-ds-and-pc/'],
        'wikipedia_links' : ['https://en.wikipedia.org/wiki/Pok%C3%A9mon_Yellow','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Gold','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Crystal','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Red_and_Blue','https://en.wikipedia.org/wiki/Mario_Kart:_Super_Circuit','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Red_and_Blue:_Special_Pikachu_Edition','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Red_and_Blue:_Special_Charizard_Edition','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Red_and_Blue:_Special_Pikachu_and_Eevee_Edition','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Sapphire_and_Ruby','https://en.wikipedia.org/wiki/Pok%C3%A9mon_Diamond_and_Pearl'],
        'image_refs' : ['/static/images/pokemon_crystal_front.png', '/static/images/pokemon_yellow_front.webp'],
        'image_mini_refs' : ['/static/images/pokemon_crystal_mini.png', '/static/images/pokemon_yellow_mini.png']
    }
    
    for i in range(len(game_junk_data['known_games'])):
        game = Game()
        game.image_mini_ref = random.choice(game_junk_data['image_mini_refs'])
        game.image_ref = random.choice(game_junk_data['image_refs'])
        game.title = game_junk_data['known_games'][i]
        game.developer = random.choice(game_junk_data['game_developers'])
        game.best_emulator = random.choice(game_junk_data['emulator_links'])
        game.extra_info = random.choice(game_junk_data['wikipedia_links'])
        game.release_date = game_junk_data['release_dates'][i]
        game.save()
    
def add_junk_categories_to_db():
    category_junk_data = {
        'image_refs' : ['/static/images/pokemon_crystal_front.png', '/static/images/pokemon_yellow_front.webp'],
    }
    for _ in range(1, 30):
        category = Category()
        category.image_ref = random.choice(category_junk_data['image_refs'])
        category.name = secrets.token_urlsafe(random.randint(5, 15))
        category.description = ' '.join([secrets.token_hex(random.randint(2, 5)) for _ in range(random.randint(10, 20))])
        category.base_game = Game.objects.order_by('?').first()
        if random.random() < 0.10:
            category.parent_category = None
        else:
            if Category.objects.exists():
                category.parent_category = Category.objects.order_by('?').first()
            else:
                category.parent_category = None
        category.save()
        
def add_junk_patch_options_to_db():
    patchoption_junk_data = {
        'code_files' : [secrets.token_urlsafe(random.randint(15, 35)) for _ in range(40)],
    }
    for _ in range(1,80):
        pOption = PatchOption()
        pOption.code_file = random.choice(patchoption_junk_data['code_files'])
        pOption.name = secrets.token_urlsafe(random.randint(5, 15))
        pOption.description = ' '.join([secrets.token_hex(random.randint(2, 5)) for _ in range(random.randint(10, 20))])
        pOption.category = random.choice(Category.objects.all())
        pOption.save()
        
def add_junk_patches_to_db():
    patch_junk_data = {
        'creators' : User.objects.order_by('?'),
        'patch_options' : list(set(random.sample(list(PatchOption.objects.all()), random.randint(5, 40))))
    }
    for _ in range (1,50):
        patch = Patch()
        patch.name = secrets.token_urlsafe(random.randint(5, 15))
        patch.downloads = random.randint(0, 1000)
        patch.favorites = random.randint(0, 1000)
        patch.creator = random.choice(patch_junk_data['creators'])
        patch.creation_date = datetime.date(datetime.date.today().year,random.randint(1,12),random.randint(1,28))
        patch.save()
        patch.patch_options.set(list(set(random.sample(list(PatchOption.objects.all()), random.randint(5, 40)))))
