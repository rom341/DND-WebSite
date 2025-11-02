from django.shortcuts import get_object_or_404, redirect, render
from battlefield.models import Character, Group, CharacterStats, CharacterMoney
from battlefield.forms.move_character_form import MoveCharacterForm
from django.contrib.auth.decorators import login_required
from battlefield.utils.ruler import ruler

# Create your views here.
@login_required
def move_character(request):
    if request.method == 'POST':
        character_id = request.POST.get('name')
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        try:
            #character_to_update = Character.objects.get(id=character_id, group=group)
            
            character_to_update = request.user.characters.get(id=character_id, group=group)
        except Character.DoesNotExist:
            print("Character does not exist in this group.")
            return render(request, 'errors.html', {'message': 'Character does not exist in this group.'})
        
        form = MoveCharacterForm(request.POST, instance=character_to_update, group=group)
        if form.is_valid():
            new_pos_x = form.cleaned_data['position_x']
            new_pos_y = form.cleaned_data['position_y']
            characters_on_position = group.characters.filter(
                position_x=new_pos_x,
                position_y=new_pos_y
            ).exclude(id=character_to_update.id)
            if not characters_on_position.exists():
                if character_to_update.movement_speed/5 < ruler(character_to_update.position_x, character_to_update.position_y, new_pos_x, new_pos_y):
                    print("Not enough movement speed.")
                    return render(request, 'errors.html', {'message': 'Not enough movement speed.'})
                    
                character_to_update.move_to(new_pos_x, new_pos_y)
                print(f"Character {character_to_update.name} moved")
                return render(request, 'partials/battle_map.html', {
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': group.characters.all(),
                })
            else:
                print("Position is occupied.")
                return render(request, 'errors.html', {'message': f'Invalid data: {form.errors.as_text()}'})
        else:
            print("Form is invalid:", form.errors)
           
            return render(request, 'errors.html', {'message': f'Invalid data: {form.errors.as_text()}'})
        
    return render(request, 'errors.html', {'message': f'Invalid data: {form.errors.as_text()}'})
    

@login_required
def battle(request):    
    group_id = request.GET.get('group_id')
    # If no group_id provided, redirect to groups page
    if not group_id:
        return redirect('groups')
    
    group = Group.objects.filter(id=group_id).first()
    if not group:
        return redirect('groups')
    
    characters = group.characters.all()    
    form = MoveCharacterForm(group=group)    
    data = {
        'rows_range': range(10),
        'cols_range': range(5),
        'characters': characters,
        'form': form,
        'group_id': group_id,
    }
    
    return render(request, 'battlefield.html', data)

@login_required
def groups(request):    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'select': # group selected
            group_id = request.POST.get('group_id')
            return redirect(f'/battle/?group_id={group_id}')
        
        elif action == 'create': # new group created
            new_group_name = request.POST.get('group_name')
            new_group = Group(name=new_group_name)
            new_group.save()
            return redirect(f'/battle/?group_id={new_group.id}')
    
    groups = Group.objects.all()    
    data = {
        'groups': groups,
    }

    return render(request, 'groups.html', data)

def main_page(request):
    return render(request, 'main_page.html')

def create_character(request):
    if request.method == 'POST':

        name = request.POST.get('character_name')
        player_name = request.POST.get('player_name')
        character_class = request.POST.get('class')
        character_sub_class = request.POST.get('subclass')
        level = request.POST.get('level')
        experience_points = request.POST.get('experience_points')

        race = request.POST.get('race')
        alignment = request.POST.get('aligment')

        size = request.POST.get('size')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        max_hit_points = request.POST.get('hit_points')
        current_hit_points = request.POST.get('hit_points')
        armor_class = request.POST.get('armor_class')
        movement_speed = request.POST.get('movement_speed')

        copper_coins = request.POST.get('copper_coins')
        silver_coins = request.POST.get('silver_coins')
        electrum_coins = request.POST.get('electrum_coins')
        gold_coins = request.POST.get('gold_coins')
        platinum_coins = request.POST.get('platinum_coins')

        strength = request.POST.get('strength')
        dexterity = request.POST.get('dexterity')
        constitution = request.POST.get('constitution')
        intelligence = request.POST.get('intelligence')
        wisdom = request.POST.get('wisdom')
        charisma = request.POST.get('charisma')

        new_money_bag = CharacterMoney.objects.create(
            copper_coins=copper_coins,
            silver_coins=silver_coins,
            electrum_coins=electrum_coins,
            gold_coins=gold_coins,
            platinum_coins=platinum_coins
        )

        new_stats =CharacterStats.objects.create(
            strength=strength, 
            dexterity=dexterity, 
            constitution=constitution, 
            intelligence=intelligence, 
            wisdom=wisdom, 
            charisma=charisma
        )

        new_character = Character.objects.create(
            user = request.user,
            name=name,
            character_class=character_class, 
            character_sub_class=character_sub_class,
            level=level,
            experience=experience_points,

            race=race,
            alignment=alignment,

            size=size,
            age=age,
            height=height,
            weight=weight,

            max_hit_points=max_hit_points,
            current_hit_points=max_hit_points,
            armor_class=armor_class, 
            movement_speed=movement_speed,

            money=new_money_bag,
            stats=new_stats

        )
        
        redirect('main_page')

    return render(request, 'create_character.html')