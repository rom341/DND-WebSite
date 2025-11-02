class CharacterStatsTemplate:
    """Шаблон характеристик персонажа с новыми полями."""

    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

class CharacterMoneyTemplate:
    """Шаблон валют персонажа с новыми полями."""

    copper_coins: int
    silver_coins: int
    electrum_coins: int
    gold_coins: int
    platinum_coins: int    

class CharacterTemplate:
    """Шаблон персонажа с новыми полями."""

    character_name: str
    character_class: str 
    character_sub_class:  str
    level: int
    experience : int

    race : str
    alignment : str

    size : str
    age : int
    height : int
    weight : int

    max_hit_points : int
    current_hit_points : int
    armor_class : int
    movement_speed : int

    character_money_template: CharacterMoneyTemplate
    character_stats_template: CharacterStatsTemplate
