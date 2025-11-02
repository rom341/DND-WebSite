from battlefield.utils.character_template import CharacterTemplate, CharacterStatsTemplate, CharacterMoneyTemplate

def longstory_character_importer(realdata):
    """Достаёт необходимые данные из json (long-story) и создаёт персонажа."""

    new_money_bag = CharacterMoneyTemplate()
    new_money_bag.copper_coins = realdata.get('coins').get('cp').get('value')
    new_money_bag.silver_coins = realdata.get('coins').get('sp').get('value')
    new_money_bag.electrum_coins = realdata.get('coins').get('ep').get('value')
    new_money_bag.gold_coins = realdata.get('coins').get('gp').get('value')
    new_money_bag.platinum_coins = realdata.get('coins').get('pp').get('value')

    new_stats = CharacterStatsTemplate()
    new_stats.strength = realdata.get('stats').get('str').get('score')
    new_stats.dexterity = realdata.get('stats').get('dex').get('score')
    new_stats.constitution = realdata.get('stats').get('con').get('score')
    new_stats.intelligence = realdata.get('stats').get('int').get('score')
    new_stats.wisdom = realdata.get('stats').get('wis').get('score')
    new_stats.charisma = realdata.get('stats').get('cha').get('score')

    new_character = CharacterTemplate()
    new_character.character_name = realdata.get('name').get('value')

    new_character.character_class = realdata.get('info').get('charClass').get('value')
    new_character.character_sub_class = realdata.get('info').get('charSubclass').get('value')
    new_character.level = realdata.get('info').get('level').get('value')
    new_character.experience = realdata.get('info').get('experience').get('value')

    new_character.race = realdata.get('info').get('race').get('value')
    new_character.alignment = realdata.get('info').get('alignment').get('value')

    new_character.size = realdata.get('info').get('size').get('value')
    new_character.age = realdata.get('subInfo').get('age').get('value')
    new_character.height = realdata.get('subInfo').get('height').get('value')
    new_character.weight = realdata.get('subInfo').get('weight').get('value')

    new_character.max_hit_points = realdata.get('vitality').get('hp-max').get('value')
    new_character.current_hit_points = realdata.get('vitality').get('hp-current').get('value')
    new_character.movement_speed = realdata.get('vitality').get('speed').get('value')
    new_character.armor_class = realdata.get('vitality').get('ac').get('value')

    new_character.character_money_template = new_money_bag
    new_character.character_stats_template = new_stats

    return new_character