from django.shortcuts import redirect, render

from lobby.models import DefaultRoles, Lobby
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.urls import reverse

# Create your views here.
@login_required
def lobby(request):
    active_user = request.user    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            with transaction.atomic(): # Ensure that the whole function is atomic (all-or-nothing)
                if action == 'select': # lobby selected
                    lobby_id = request.POST.get('lobby_id')  
                elif action == 'create': # new lobby created
                    new_lobby_name = request.POST.get('lobby_name')
                    new_lobby = Lobby.objects.create_lobby(new_lobby_name)
                    Lobby.objects.add_user_to_lobby(active_user, new_lobby, role_name=DefaultRoles.GAME_MASTER.value)
                    lobby_id = new_lobby.id
                    
                if lobby_id:
                    request.session['current_lobby_id'] = lobby_id
                    return redirect(reverse('battlefield'))
                else:
                    messages.error(request, "Lobby is not valid")
                    
        except Exception as e:
            messages.error(request, f"Unknown error while operating lobby selection page: {str(e)}")
            return redirect(reverse('lobby'))
        
    lobby = Lobby.objects.get_lobby_with_user(active_user)   
    data = {
        'lobby': lobby,
    }

    return render(request, 'lobby.html', data)