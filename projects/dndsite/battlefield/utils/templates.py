class CharacterSpellsTemplate:
    """ Шаблон заклинаний персонажа """

    spell_name: str
    """ Название скила """
    atack_roll: str
    """ Бросок атаки """
    damage_dice: str
    """ Кубик урона """
    damage_dice_count: int
    """ Количество кубиков урона"""
    damage_modificator: int
    """Модификатор урона"""
    saving_throw: str
    """Спасбросок"""
    is_using_spell_circle: bool=True
    """Нужна ли скилу ячейка заклинаний"""
    required_spell_circle: int
    """Минимальная ячейка необходимая для скила"""


class CharacterSkillsTemplate:
    """ Шаблон скилов персонажа """

    skill_name: str
    """Название заклинания"""
    atack_roll: str
    """ Бросок атаки """
    damage_dice: str
    """ Кубик урона """
    damage_dice_count: int
    """ Количество кубиков урона"""
    damage_modificator: int
    """Модификатор урона"""
    saving_throw: str
    """Спасбросок"""
    is_using_spell_circle: bool=False
    """Нужна ли ячейка заклинаний"""
    required_spell_circle: int
    """Минимальная ячейка необходимая для заклинания"""


class CharacterSpellCirclesSlotsTemplate:
    """Шаблон кругов заклинаний персонажа с новыми полями."""

    circle_1: int
    """Первый круг заклинаний"""
    circle_2: int
    """Второй круг заклинаний"""
    circle_3: int
    """Третий круг заклинаний"""
    circle_4: int
    """Четвёртый круг заклинаний"""
    circle_5: int
    """Пятый круг заклинаний"""
    circle_6: int
    """Шестой круг заклинаний"""
    circle_7: int
    """Седьмой круг заклинаний"""
    circle_8: int
    """Восьмой круг заклинаний"""
    circle_9: int
    """Девятый круг заклинаний"""

class CharacterStatsTemplate:
    """Шаблон характеристик персонажа с новыми полями."""

    strength: int
    """СИИЛА"""
    dexterity: int
    """ЛОВКОСТЬ"""
    constitution: int
    """ТЕЛОСЛОЖЕНИЕ"""
    intelligence: int
    """ИНТЕЛЛЕКТ"""
    wisdom: int
    """МУДРОСТЬ"""
    charisma: int
    """ХАРИЗМА"""

class CharacterMoneyTemplate:
    """Шаблон валют персонажа с новыми полями."""

    copper_coins: int
    """Медные монеты"""
    silver_coins: int
    """Серебряные монеты"""
    electrum_coins: int
    """Электрумовые монеты"""
    gold_coins: int
    """Золотые монеты"""
    platinum_coins: int
    """Платиновые монеты"""

class CharacterTemplate:
    """Шаблон персонажа с новыми полями."""
    def __str__(self):
        return f"{self.character_name}, Level {self.level} {self.character_class}/{self.character_sub_class}/{self.age}"
    character_name: str
    """Имя персонажа"""
    character_class: str
    """Класс персонажа""" 
    character_sub_class:  str
    """Специализация персонажа"""
    level: int
    """Уровень персонажа"""
    experience : int
    """Количество опыта персонажа"""

    race : str
    """Раса персонажа"""
    alignment : str
    """Мировоззрение персонажа"""

    size : str
    """Размер персонажа"""
    age : int
    """Возраст персонажа"""
    height : int
    """Рост персонажа"""
    weight : int
    """Вес персонажа"""

    max_hit_points : int
    """Максимальные ХП персонажа"""
    current_hit_points : int
    """Текущие ХП персонажа"""
    armor_class : int
    """Класс брони персонажа"""
    movement_speed : int
    """Скорость передвижения персонажа"""

    character_money_template: CharacterMoneyTemplate
    """Кошелёк персонажа"""
    character_stats_template: CharacterStatsTemplate
    """Статы персонажа"""
    mastery: int
    """Бонус мастерства персонажа"""
    character_spell_circle_slots_template: CharacterSpellCirclesSlotsTemplate
    """Круги и кол-во ячеек заклинания данного круга персонажа"""
