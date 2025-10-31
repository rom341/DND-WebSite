from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth 
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        #TODO replace with django forms
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2 and not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('battle')
            #return redirect('login')
        else:
            #stay on the same page
            messages.info(request, 'Password not matching or username/email taken')
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('battle')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER','/')) # stay on the same page
    