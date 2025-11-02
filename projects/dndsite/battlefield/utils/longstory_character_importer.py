from battlefield.utils.character_template import CharacterTemplate, CharacterStatsTemplate, CharacterMoneyTemplate

def longstory_character_importer(data):
    """Достаёт необходимые данные из json (long-story) и создаёт персонажа."""

    new_money_bag = CharacterMoneyTemplate()
    new_money_bag.copper_coins = data.get('coins').get('cp').get('value')
    new_money_bag.silver_coins = data.get('coins').get('sp').get('value')
    new_money_bag.electrum_coins = data.get('coins').get('ep').get('value')
    new_money_bag.gold_coins = data.get('coins').get('gp').get('value')
    new_money_bag.platinum_coins = data.get('coins').get('pp').get('value')

    new_stats = CharacterStatsTemplate()
    new_stats.strength = data.get('stats').get('str').get('score')
    new_stats.dexterity = data.get('stats').get('dex').get('score')
    new_stats.constitution = data.get('stats').get('con').get('score')
    new_stats.intelligence = data.get('stats').get('int').get('score')
    new_stats.wisdom = data.get('stats').get('wis').get('score')
    new_stats.charisma = data.get('stats').get('cha').get('score')

    new_character = CharacterTemplate()
    new_character.character_name = data.get('name').get('value')

    new_character.character_class = data.get('info').get('charClass').get('value')
    new_character.character_sub_class = data.get('info').get('charSubclass').get('value')
    new_character.level = data.get('info').get('level').get('value')
    new_character.experience = data.get('info').get('experience').get('value')

    new_character.race = data.get('info').get('race').get('value')
    new_character.alignment = data.get('info').get('alignment').get('value')

    new_character.size = data.get('info').get('size').get('value')
    new_character.age = data.get('subInfo').get('age').get('value')
    new_character.height = data.get('subInfo').get('height').get('value')
    new_character.weight = data.get('subInfo').get('weight').get('value')

    new_character.max_hit_points = data.get('vitality').get('hp-max').get('value')
    new_character.current_hit_points = data.get('vitality').get('hp-current').get('value')
    new_character.movement_speed = data.get('vitality').get('speed').get('value')
    new_character.armor_class = data.get('vitality').get('ac').get('value')

    new_character.character_money_template = new_money_bag
    new_character.character_stats_template = new_stats

    print('all good, creating character...')

    return new_character