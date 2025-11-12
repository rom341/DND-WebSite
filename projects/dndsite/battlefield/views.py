from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from battlefield.forms.add_character_to_group_form import AddCharacterToGroupForm
from battlefield.forms.add_user_to_group_form import AddUserToGroupForm
from battlefield.forms.uploading_json_files_form import JsonUploadForm
from battlefield.models import Character, CharacterSkills, CharacterSpells, Group, CharacterStats, CharacterMoney, GroupMembershipUser
from battlefield.forms.move_character_form import MoveCharacterForm
from django.contrib.auth.decorators import login_required
from battlefield.utils.decorators import game_master_required
from battlefield.utils.model_managers.group_manager import GroupManager
from battlefield.utils.model_managers.user_manager import UserManager
from django.db import transaction

from battlefield.utils.longstory_character_importer import longstory_character_importer
import json

from battlefield.utils.model_managers.role_manager import DefaultRoles
from battlefield.utils.templates import CharacterSkillsTemplate, CharacterSpellsTemplate

# Create your views here.
@game_master_required
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
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group),
                    'add_character_form': form
                }
                return render(request, 'partials/battle_map.html', context)
    else:
        form = AddCharacterToGroupForm()

    return render(request, 'partials/battle_map.html', {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group) if group else [],
                    'add_character_form': form
                })

@game_master_required
def add_user_to_group(request):
    print("Entered add_user_to_group view")
    if request.method == 'POST':
        print("Processing AddUserToGroupForm submission")
        group_id = request.POST.get('group_id')
        group = GroupManager.get_group_by_id(group_id)
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        print(f"Retrieved group: {group} and user: {user.username}")
        form = AddUserToGroupForm(request.POST, group=group)
        if form.is_valid():
            print("Form is valid")
            if group:
                print(f"Adding user {user.username} to group {group.name}")
                GroupManager.add_user_to_group(user, group)
                context = {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group),
                    'add_user_form': form
                }
                return render(request, 'partials/battle_map.html', context)
    else:
        form = AddUserToGroupForm()

    return render(request, 'partials/battle_map.html', {
                    'rows_count': 10,
                    'cols_count': 5,
                    'rows_range': range(10),
                    'cols_range': range(5),
                    'characters': GroupManager.get_characters_in_group(group) if group else [],
                    'add_user_form': form
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
        print("No group_id provided in request.")
        return redirect('groups')

    group = GroupManager.get_group_by_id(group_id)
    if not group:
        print(f"Group with ID {group_id} not found.")
        return redirect('groups')
    
    characters = GroupManager.get_characters_in_group(group) 
    print(f"Group {group.name} has characters: {', '.join(c.name for c in characters)}")
    move_character_form = MoveCharacterForm(group=group)    
    add_character_form = AddCharacterToGroupForm(group=group)
    add_user_form = AddUserToGroupForm(group=group)
    data = {
        'rows_count': 10,
        'cols_count': 5,
        'rows_range': range(10),
        'cols_range': range(5),
        'characters': characters,
        'move_character_form': move_character_form,
        'add_character_form': add_character_form,
        'add_user_form':add_user_form,
        'group_id': group_id,
    }
    
    return render(request, 'battlefield.html', data)

@login_required
def groups(request):
    user = request.user    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            with transaction.atomic(): # Ensure that the whole function is atomic (all-or-nothing)
                if action == 'select': # group selected
                    group_id = request.POST.get('group_id')
                    group = GroupManager.get_group_by_id(group_id)
                    characters = GroupManager.get_characters_in_group(group)
                    return redirect(f'/battle/?group_id={group_id}')
                
                elif action == 'create': # new group created
                    new_group_name = request.POST.get('group_name')
                    new_group = Group(name=new_group_name)
                    new_group.save()
                    GroupManager.add_user_to_group(user, new_group, role_name=DefaultRoles.GAME_MASTER.value)
                    return redirect(f'/battle/?group_id={new_group.id}')
        except Exception as e:
            print(f"Error processing group action '{action}': {e}")
        
    groups = GroupManager.get_groups_with_user(user)   
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

def create_skill(request):
    if request.method == 'POST':
        skill = CharacterSkillsTemplate()
        skill.skill_name =  request.POST.get('skill_name')
        skill.atack_roll = request.POST.get('atack_roll')
        skill.damage_dice = request.POST.get('damage_dice')
        skill.damage_dice_count = request.POST.get('damage_dice_count')
        skill.damage_modificator = request.POST.get('damage_modificator')
        skill.saving_throw = request.POST.get('saving_throw')
        skill.is_using_spell_circle = 'is_using_spell_circle' in request.POST
        skill.required_spell_circle =request.POST.get('required_spell_circle')
        new_skill = CharacterSkills()
        new_skill.create_from_template(skill)
        return redirect('main_page')
    
    return render(request,'create_skill.html' )

def create_spell(request):
    if request.method == 'POST':
        spell = CharacterSpellsTemplate()
        spell.spell_name =  request.POST.get('spell_name')
        spell.atack_roll = request.POST.get('atack_roll')
        spell.damage_dice = request.POST.get('damage_dice')
        spell.damage_dice_count = request.POST.get('damage_dice_count')
        spell.damage_modificator = request.POST.get('damage_modificator')
        spell.saving_throw = request.POST.get('saving_throw')
        spell.is_using_spell_circle = True
        spell.required_spell_circle =request.POST.get('required_spell_circle')
        new_spell= CharacterSpells()
        new_spell.create_from_template(spell)
        return redirect('main_page')
     
    return render(request,'create_spell.html')


def my_characters_list(request):
    user = request.user
    all_user_characters = UserManager.get_user_characters(user)
    data = {
        'all_user_characters': all_user_characters
    }
    return render(request,'my_characters_list.html',data)
    