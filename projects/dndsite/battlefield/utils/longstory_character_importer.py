import json
from battlefield.models import Character, CharacterStats

def longstory_charcter_importer(realdata):
    """Достаёт необходимые данные из json (long-story) и создаёт персонажа."""

    name = realdata.get('name').get('value')

    character_class = realdata.get('info').get('charClass').get('value')
    character_sub_class = realdata.get('info').get('charSubclass').get('value')
    level = realdata.get('info').get('level').get('value')
    player_name = realdata.get('info').get('playerName').get('value')
    race = realdata.get('info').get('race').get('value')
    alignment = realdata.get('info').get('alignment').get('value')
    experience = realdata.get('info').get('experience').get('value')
    size = realdata.get('info').get('size').get('value')

    age = realdata.get('subInfo').get('age').get('value')
    height = realdata.get('subInfo').get('height').get('value')
    weight = realdata.get('subInfo').get('weight').get('value')

    max_hit_points = realdata.get('vitality').get('hp-max').get('value')
    current_hit_points = realdata.get('vitality').get('hp-current').get('value')
    movement_speed = realdata.get('vitality').get('speed').get('value')
    armor_class = realdata.get('vitality').get('ac').get('value')

    copper_coins = realdata.get('coins').get('cp').get('value')
    silver_coins = realdata.get('coins').get('sp').get('value')
    electrum_coins = realdata.get('coins').get('ep').get('value')
    gold_coins = realdata.get('coins').get('gp').get('value')
    platinum_coins = realdata.get('coins').get('pp').get('value')

    str = realdata.get('stats').get('str').get('score')
    dex = realdata.get('stats').get('dex').get('score')
    con = realdata.get('stats').get('con').get('score')
    intt = realdata.get('stats').get('int').get('score')
    wis = realdata.get('stats').get('wis').get('score')
    cha = realdata.get('stats').get('cha').get('score')

   
    new_stats =CharacterStats.objects.create(
            strength=str, 
            dexterity=dex, 
            constitution=con, 
            intelligence=intt, 
            wisdom=wis, 
            charisma=cha
        )
    new_character = Character.objects.create(
        name=name,
        stats=new_stats,
        character_class=character_class,
        character_sub_class=character_sub_class,
        max_hit_points=max_hit_points,
        current_hit_points=current_hit_points,
        armor_class=armor_class,
        movement_speed=movement_speed
    )

    return new_character