from django.shortcuts import redirect, render
from battlefield.forms.add_character_to_group_form import AddCharacterToGroupForm
from battlefield.forms.uploading_json_files_form import JsonUploadForm
from battlefield.models import Character, Group, CharacterStats, CharacterMoney
from battlefield.forms.move_character_form import MoveCharacterForm
from django.contrib.auth.decorators import login_required
from battlefield.utils.group_manager import GroupManager
from battlefield.utils.longstory_character_importer import longstory_character_importer
import json


# Create your views here.
def add_character_to_group(request):
    if request.method == 'POST':
        print("Processing AddCharacterToGroupForm submission")
        group_id = request.POST.get('group_id')
        group = GroupManager.get_group_by_id(group_id)
        character_id = request.POST.get('character_id')
        character = Character.objects.get(id=character_id)
        print(f"Retrieved group: {group} and character ID: {character_id}")
        form = AddCharacterToGroupForm(request.POST, group=group)
        if form.is_valid():
            print("Form is valid")
            if group:
                print(f"Adding character {character.name} to group {group.name}")
                GroupManager.add_character_to_group(character, group)
                context = {
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group),
                    'add_character_form': form
                }
                return render(request, 'partials/battle_map.html', context)
    else:
        form = AddCharacterToGroupForm()

    return render(request, 'partials/battle_map.html', {
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group) if group else [],
                    'add_character_form': form
                })

@login_required
def upload_longstory_character_json(request):
    print("Entered upload_longstory_character_json view")
    if request.method == 'POST':
        form = JsonUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['json_file']

            file_content = json_file.read().decode('utf-8')
            data = json.loads(json.loads(file_content).get('data'))
            new_character_template = longstory_character_importer(data)
            new_character = Character()
            new_character.user = request.user
            print('==============================')
            print(new_character_template)
            new_character = new_character.create_form_template(new_character_template)
            new_character.save()
            return redirect('groups')
        else:
            pass
    else:
        form = JsonUploadForm()
    return render(request, 'create_character.html', {'upload_json_files_form': form})

@login_required
def battle(request):    
    group_id = request.GET.get('group_id')
    # If no group_id provided, redirect to groups page
    if not group_id:
        return redirect('groups')

    group = GroupManager.get_group_by_id(group_id)
    if not group:
        return redirect('groups')
    
    characters = GroupManager.get_characters_in_group(group) 
    print(f"Group {group.name} has characters: {', '.join(c.name for c in characters)}")
    move_character_form = MoveCharacterForm(group=group)    
    add_character_form = AddCharacterToGroupForm(group=group)
    data = {
        'rows_range': range(10),
        'cols_range': range(5),
        'characters': characters,
        'move_character_form': move_character_form,
        'add_character_form': add_character_form,
        'group_id': group_id,
    }
    
    return render(request, 'battlefield.html', data)

@login_required
def groups(request):    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'select': # group selected
            group_id = request.POST.get('group_id')
            group = GroupManager.get_group_by_id(group_id)
            characters = GroupManager.get_characters_in_group(group)
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

        print('============================')
        print(copper_coins, silver_coins, electrum_coins, gold_coins, platinum_coins)
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
        
        
        return redirect('main_page')
        
    uploadform = JsonUploadForm()
    print(uploadform)
    data = {
        'upload_json_files_form': uploadform
    }

    return render(request, 'create_character.html', data)