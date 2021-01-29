from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect

def index(request, param=""):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'index.html', {"param": param})


def appLogin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["login"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Zalogowano pomyslnie")
            else:
                messages.warning(request, "Wprowadzono bledne dane")
    if request.user.is_authenticated:
        # return render(request, 'login.html')
        return redirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def appReg(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST["login"]
            email = request.POST["email"]
            password = request.POST["password"]
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
                messages.success(request, "Udalo sie stworzyc nowe konto")
            else:
                messages.warning(request, "Uzytkownik istnieje w bazie")
    if not request.user.is_authenticated:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    else:
        return redirect('/login')
