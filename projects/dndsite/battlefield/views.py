from django.shortcuts import get_object_or_404, redirect, render
from battlefield.models import Group
from battlefield.forms.move_character_form import MoveCharacterForm

# Create your views here.
def battle(request):    
    print("Battle View Accessed")
    group = get_object_or_404(Group, pk=1)
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