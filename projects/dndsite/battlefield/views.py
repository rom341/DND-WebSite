from django.shortcuts import get_object_or_404, redirect, render
from battlefield.models import Group
from battlefield.forms.move_character_form import MoveCharacterForm

# Create your views here.
def battle(request):    
    group_id = request.GET.get('group_id')
    group = Group.objects.get(id=group_id)
    characters = group.characters.all()
    
    form = MoveCharacterForm()
    if request.method == 'POST':
        form = MoveCharacterForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.group = group
            
            message.save()
            print(f"Character moved to ({message.position_x}, {message.position_y})")
            return redirect('battle')
        
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