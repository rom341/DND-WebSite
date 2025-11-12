import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounts.utils.managers.user_manager import UserManager
from characters.forms.uploading_json_files_form import JsonUploadForm
from characters.models import Character, CharacterMoney, CharacterSkills, CharacterSpells, CharacterStats
from characters.templates import CharacterSkillsTemplate, CharacterSpellsTemplate
from characters.utils.importers.longstory_character_importer import longstory_character_importer

    

# Create your views here.
@login_required
def upload_longstory_character_json(request):
    if request.method == 'POST':
        form = JsonUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['json_file']

            file_content = json_file.read().decode('utf-8')
            data = json.loads(json.loads(file_content).get('data'))
            new_character_template = longstory_character_importer(data)
            new_character = Character()
            new_character.user = request.user
            new_character = new_character.create_form_template(new_character_template)
            new_character.save()
            return redirect('groups')
        else:
            pass
    else:
        form = JsonUploadForm()
    return render(request, 'create_character.html', {'upload_json_files_form': form})

def create_character(request):
    #TODO: rework this
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

        new_stats = CharacterStats.objects.create(
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