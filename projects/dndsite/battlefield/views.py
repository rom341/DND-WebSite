from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from battlefield.models import Group
from battlefield.forms.move_character_form import MoveCharacterForm

# Create your views here.
def battle(request):
    group = get_object_or_404(Group, pk=1)
    characters = group.characters.all()
    data = {
        'extra_text': 'Roman',
        'rows_range': range(10),
        'cols_range': range(5),
        'characters': characters,
    }
    
    form = MoveCharacterForm()
    return render(request, 'battlefield.html', data)