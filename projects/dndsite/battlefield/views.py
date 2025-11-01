from django.shortcuts import get_object_or_404, redirect, render
from battlefield.models import Character, Group
from battlefield.forms.move_character_form import MoveCharacterForm

# Create your views here.
def battle(request):    
    group_id = request.GET.get('group_id')
    group = get_object_or_404(Group, id=group_id)
    characters = group.characters.all()
    
    form = MoveCharacterForm()
    if request.method == 'POST':
        character_id = request.POST.get('character_to_move')
        
        try:
            character_to_update = Character.objects.get(id=character_id, group=group)
        except:
            return redirect(f"{request.path}?group_id={group_id}")
        
        form = MoveCharacterForm(request.POST, instance=character_to_update)
        
        """
        if character_new_position == isEmpty():
            form.save()
            
            print(f"Character {character_to_update.name} moved")
            return redirect(f"{request.path}?group_id={group_id}")
        else:
            #вывод ошибки через логику JS
        """

        if form.is_valid():
            form.save()
            
            print(f"Character {character_to_update.name} moved")
            return redirect(f"{request.path}?group_id={group_id}")

    data = {
        'rows_range': range(10),
        'cols_range': range(5),
        'characters': characters,
        'form': form,
    }
    
    return render(request, 'battlefield.html', data)

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