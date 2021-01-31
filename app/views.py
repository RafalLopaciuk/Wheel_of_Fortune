from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Player, Server
from django.forms.models import model_to_dict


def index(request):
    if request.user.is_authenticated:
        servers = Server.objects.all().order_by('-create_date')
        return render(request, 'index.html', {"servers": servers})
    else:
        return render(request, 'index.html')


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
                Player.objects.create(user=user)
                messages.success(request, "Udalo sie stworzyc nowe konto")
                return redirect('/login')
            else:
                messages.warning(request, "Uzytkownik istnieje w bazie")
    if not request.user.is_authenticated:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    else:
        return redirect('/')


def accountDetails(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        player = Player.objects.get(user=request.user)
        return render(request, 'account.html', {'player': player})


def createServer(request):
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
                Player.objects.create(user=user)
                messages.success(request, "Udalo sie stworzyc nowe konto")
                return redirect('/login')
            else:
                messages.warning(request, "Uzytkownik istnieje w bazie")
    if not request.user.is_authenticated:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    else:
        return redirect('/')