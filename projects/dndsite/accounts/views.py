from django.shortcuts import redirect, render

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
def main_page(request):
    return render(request, 'main_page.html')
    