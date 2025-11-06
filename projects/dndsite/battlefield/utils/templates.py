class CharacterSpellCirclesSlotsTemplate:
    """Шаблон кругов заклинаний персонажа с новыми полями."""

    circle_1: int
    circle_2: int
    circle_3: int
    circle_4: int
    circle_5: int
    circle_6: int
    circle_7: int
    circle_8: int
    circle_9: int

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
    def __str__(self):
        return f"{self.character_name}, Level {self.level} {self.character_class}/{self.character_sub_class}/{self.age}"
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
    character_spell_circle_slots_template: CharacterSpellCirclesSlotsTemplate
