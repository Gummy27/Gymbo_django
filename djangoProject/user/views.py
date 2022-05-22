from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    form = AuthenticationForm()

    return render(request, 'user/login.html', context={'form': form})


def signup(request):
    if request.method == 'POST':
        print("This is coming here!")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)

            login(request, user)

            return redirect('home')

    form = UserCreationForm()

    return render(request, 'user/signup.html', context={'form': form})


def signout(request):
    logout(request)
    return redirect('home')


def change(request):
    pass


def update(request):
    pass

