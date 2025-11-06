import random

def dice_roller(dice_notation):
    """ Кидает кости согласно нотации в формате 'NdM', где N - количество костей, M - количество граней на каждой кости."""

    try:
        parts = dice_notation.split('d')
        if parts[0] == '':
            num_dice = 1
        else:
            num_dice = int(parts[0])

        num_face = int(parts[1])

        if num_dice <= 0 or num_face <= 0:
            return [], 0
        
        rolls = []
        summa = 0

        for _ in range(num_dice):
            roll = random.randint(1, num_face)
            rolls.append(roll)
            summa += roll

        return rolls, summa
        
    except(ValueError, IndexError):
        return [], 0
    