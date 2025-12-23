from attr import dataclass
from django.contrib.auth.models import User

@dataclass
class CharacterSpellsTemplate:
    """ Шаблон заклинаний персонажа """

    spell_name: str = None
    """ Название заклинания """
    atack_roll: str = None
    """ Бросок атаки """
    damage_dice: str = None
    """ Кубик урона """
    damage_dice_count: int = 0
    """ Количество кубиков урона"""
    damage_modificator: int = 0
    """Модификатор урона"""
    saving_throw: str = None
    """Спасбросок"""
    required_spell_circle: int = 0
    """Минимальная ячейка необходимая для заклинания"""
    is_using_spell_circle: bool=True
    """Нужна ли скилу ячейка заклинаний"""

@dataclass
class CharacterSkillsTemplate:
    """ Шаблон скилов персонажа """

    skill_name: str = None
    """Название навыка"""
    atack_roll: str = None
    """ Бросок атаки """
    damage_dice: str = None
    """ Кубик урона """
    damage_dice_count: int = 0
    """ Количество кубиков урона"""
    damage_modificator: int = 0
    """Модификатор урона"""
    saving_throw: str = None
    """Спасбросок"""
    required_spell_circle: int = 0
    """Минимальная ячейка необходимая для навыка"""
    is_using_spell_circle: bool=False
    """Нужна ли ячейка заклинаний"""

@dataclass
class CharacterSpellCirclesSlotsTemplate:
    """Шаблон кругов заклинаний персонажа с новыми полями."""

    circle_1: int = 0
    """Первый круг заклинаний"""
    circle_2: int = 0
    """Второй круг заклинаний"""
    circle_3: int = 0
    """Третий круг заклинаний"""
    circle_4: int = 0
    """Четвёртый круг заклинаний"""
    circle_5: int = 0
    """Пятый круг заклинаний"""
    circle_6: int = 0
    """Шестой круг заклинаний"""
    circle_7: int = 0
    """Седьмой круг заклинаний"""
    circle_8: int = 0
    """Восьмой круг заклинаний"""
    circle_9: int = 0
    """Девятый круг заклинаний"""

@dataclass
class CharacterStatsTemplate:
    """Шаблон характеристик персонажа с новыми полями."""

    strength: int = 0
    """СИИЛА"""
    dexterity: int = 0
    """ЛОВКОСТЬ"""
    constitution: int = 0
    """ТЕЛОСЛОЖЕНИЕ"""
    intelligence: int = 0
    """ИНТЕЛЛЕКТ"""
    wisdom: int = 0
    """МУДРОСТЬ"""
    charisma: int = 0
    """ХАРИЗМА"""

@dataclass
class CharacterMoneyTemplate:
    """Шаблон валют персонажа с новыми полями."""

    copper_coins: int = 0
    """Медные монеты"""
    silver_coins: int = 0
    """Серебряные монеты"""
    electrum_coins: int = 0
    """Электрумовые монеты"""
    gold_coins: int = 0
    """Золотые монеты"""
    platinum_coins: int = 0
    """Платиновые монеты"""

@dataclass
class EntityBaseTemplate:
    character_name: str = None
    """Имя персонажа"""
    character_class: str = None
    """Класс персонажа""" 
    character_sub_class:  str = None
    """Специализация персонажа"""
    race : str = None
    """Раса персонажа"""
    alignment : str = None
    """Мировоззрение персонажа"""
    size : str = None
    """Размер персонажа"""
    age : int = 0
    """Возраст персонажа"""
    height : int = 0
    """Рост персонажа"""
    weight : int = 0
    """Вес персонажа"""
    mastery: int = 0
    """Бонус мастерства персонажа"""
    max_hit_points : int = 0
    """Текущие ХП персонажа"""
    armor_class : int = 0
    """Класс брони персонажа"""
    movement_speed : int = 0
    """Скорость передвижения персонажа"""

@dataclass
class CharacterTemplate:
    """Шаблон персонажа с новыми полями."""
    def __str__(self):
        return f"{self.character_name}, Level {self.level} {self.character_class}/{self.character_sub_class}/{self.age}"
    
    user: User = None
    entity_base: EntityBaseTemplate = None
    """Владелец персонажа"""
    level: int = 0
    """Уровень персонажа"""
    experience : int = 0
    """Количество опыта персонажа"""
    current_hit_points : int = 0
    """Максимальные ХП персонажа"""
    money: CharacterMoneyTemplate = None
    """Кошелёк персонажа"""
    stats: CharacterStatsTemplate = None
    """Статы персонажа"""
    spell_circle_slots: CharacterSpellCirclesSlotsTemplate = None
    """Круги и кол-во ячеек заклинания данного круга персонажа"""
