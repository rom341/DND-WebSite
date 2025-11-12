from characters.templates import CharacterTemplate, CharacterStatsTemplate, CharacterMoneyTemplate, CharacterSpellCirclesSlotsTemplate

def longstory_character_importer(data):
    """Достаёт необходимые данные из json (long-story) и создаёт персонажа."""

    new_spell_circles_slots = CharacterSpellCirclesSlotsTemplate()
    new_spell_circles_slots.circle_1 = data.get('spells',{}).get('slots-1',{}).get('value',0)
    new_spell_circles_slots.circle_2 = data.get('spells',{}).get('slots-2',{}).get('value',0)
    new_spell_circles_slots.circle_3 = data.get('spells',{}).get('slots-3',{}).get('value',0)
    new_spell_circles_slots.circle_4 = data.get('spells',{}).get('slots-4',{}).get('value',0)
    new_spell_circles_slots.circle_5 = data.get('spells',{}).get('slots-5',{}).get('value',0)
    new_spell_circles_slots.circle_6 = data.get('spells',{}).get('slots-6',{}).get('value',0)
    new_spell_circles_slots.circle_7 = data.get('spells',{}).get('slots-7',{}).get('value',0)
    new_spell_circles_slots.circle_8 = data.get('spells',{}).get('slots-8',{}).get('value',0)
    new_spell_circles_slots.circle_9 = data.get('spells',{}).get('slots-9',{}).get('value',0)

    new_money_bag = CharacterMoneyTemplate()
    new_money_bag.copper_coins = data.get('coins',{}).get('cp',{}).get('value',0)
    new_money_bag.silver_coins = data.get('coins',{}).get('sp',{}).get('value',0)
    new_money_bag.electrum_coins = data.get('coins',{}).get('ep',{}).get('value',0)
    new_money_bag.gold_coins = data.get('coins',{}).get('gp',{}).get('value',0)
    new_money_bag.platinum_coins = data.get('coins',{}).get('pp',{}).get('value',0)

    new_stats = CharacterStatsTemplate()
    new_stats.strength = data.get('stats',{}).get('str',{}).get('score',10)
    new_stats.dexterity = data.get('stats',{}).get('dex',{}).get('score',10)
    new_stats.constitution = data.get('stats',{}).get('con',{}).get('score',10)
    new_stats.intelligence = data.get('stats',{}).get('int',{}).get('score',10)
    new_stats.wisdom = data.get('stats',{}).get('wis',{}).get('score',10)
    new_stats.charisma = data.get('stats',{}).get('cha',{}).get('score',10)

    new_character = CharacterTemplate()
    new_character.character_name = data.get('name',{}).get('value',None)

    new_character.character_class = data.get('info',{}).get('charClass',{}).get('value',None)
    new_character.character_sub_class = data.get('info',{}).get('charSubclass',{}).get('value',None)
    new_character.level = data.get('info',{}).get('level',{}).get('value',1)
    new_character.experience = data.get('info',{}).get('experience',{}).get('value',0)
    if not new_character.experience:
        new_character.experience = 0

    new_character.race = data.get('info',{}).get('race',{}).get('value',None)
    new_character.alignment = data.get('info',{}).get('alignment',{}).get('value',None)

    new_character.size = data.get('info',{}).get('size',{}).get('value',None)
    new_character.age = data.get('subInfo',{}).get('age',{}).get('value',0)
    if not new_character.age:
        new_character.age = 0
    new_character.height = data.get('subInfo',{}).get('height',{}).get('value',0)
    new_character.weight = data.get('subInfo',{}).get('weight',{}).get('value',0)

    new_character.max_hit_points = data.get('vitality',{}).get('hp-max',{}).get('value',0)
    new_character.current_hit_points = data.get('vitality',{}).get('hp-current',{}).get('value',0)
    new_character.movement_speed = data.get('vitality',{}).get('speed',{}).get('value',30)
    new_character.armor_class = data.get('vitality',{}).get('ac',{}).get('value',10)

    new_character.character_money_template = new_money_bag
    new_character.character_stats_template = new_stats
    new_character.character_spell_circle_slots_template = new_spell_circles_slots


    return new_character