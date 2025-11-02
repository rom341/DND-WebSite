from django.shortcuts import get_object_or_404, redirect, render
from battlefield.forms.add_character_to_group_form import AddCharacterToGroupForm
from battlefield.models import Character, Group, CharacterStats
from battlefield.forms.move_character_form import MoveCharacterForm
from django.contrib.auth.decorators import login_required
from battlefield.utils.group_manager import GroupManager
from battlefield.utils.ruler import ruler

# Create your views here.
@login_required
def move_character(request):
    # if request.method == 'POST':
    #     character_id = request.POST.get('name')
    #     group_id = request.POST.get('group_id')
    #     group = get_object_or_404(Group, id=group_id)
    #     try:
    #         #character_to_update = Character.objects.get(id=character_id, group=group)
            
    #         character_to_update = request.user.characters.get(id=character_id, group=group)
    #     except Character.DoesNotExist:
    #         print("Character does not exist in this group.")
    #         return render(request, 'errors.html', {'message': 'Character does not exist in this group.'})
        
    #     form = MoveCharacterForm(request.POST, instance=character_to_update, group=group)
    #     if form.is_valid():
    #         new_pos_x = form.cleaned_data['position_x']
    #         new_pos_y = form.cleaned_data['position_y']
    #         if not GroupManager.is_position_occupied(group, new_pos_x, new_pos_y):
    #             if character_to_update.movement_speed/5 < ruler(character_to_update.position_x, character_to_update.position_y, new_pos_x, new_pos_y):
    #                 print("Not enough movement speed.")
    #                 return render(request, 'errors.html', {'message': 'Not enough movement speed.'})
                    
    #             character_to_update.move_to(new_pos_x, new_pos_y)
    #             print(f"Character {character_to_update.name} moved")
    #             return render(request, 'partials/battle_map.html', {
    #                 'rows_range': range(10),
    #                 'cols_range': range(5),
    #                 'characters': group.characters.all(),
    #             })
    #         else:
    #             print("Position is occupied.")
    #             return render(request, 'errors.html', {'message': f'Invalid data: {form.errors.as_text()}'})
    #     else:
    #         print("Form is invalid:", form.errors)
           
    #         return render(request, 'errors.html', {'message': f'Invalid data: {form.errors.as_text()}'})
        
    return render(request, 'errors.html', {'message': f'Invalid data: {form.errors.as_text()}'})

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
        strength = request.POST.get('strength')
        dexterity = request.POST.get('dexterity')
        constitution = request.POST.get('constitution')
        intelligence = request.POST.get('intelligence')
        wisdom = request.POST.get('wisdom')
        charisma = request.POST.get('charisma')

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
            stats = new_stats,
            name=name,
            character_class=character_class, 
            character_sub_class=character_sub_class
        )
        
        redirect('main_page')

    return render(request, 'create_character.html')