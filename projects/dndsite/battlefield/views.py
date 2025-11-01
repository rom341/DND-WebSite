from django.shortcuts import get_object_or_404, redirect, render
from battlefield.models import Character, Group
from battlefield.forms.move_character_form import MoveCharacterForm
from django.contrib.auth.decorators import login_required

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
            return render(request, 'partials/error.html', {'message': 'Character does not exist in this group.'})
        
        form = MoveCharacterForm(request.POST, instance=character_to_update, group=group)        
        if form.is_valid():
            form.save()
            print(f"Character {character_to_update.name} moved")
            return render(request, 'partials/battle_map.html', {
                'rows_range': range(10),
                'cols_range': range(5),
                'characters': group.characters.all(),
            })
    
    return redirect('battle')
    

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