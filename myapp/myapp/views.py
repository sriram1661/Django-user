from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from myapp.forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignupForm()
        if request.method=="POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data["username"]
                messages.success(request, "Account created for "+user)
                return redirect('login')
        context = {"form" : form}
        return render(request,"signup.html",context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = LoginForm()
        if request.method=="POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username or password is incorrect")
        context = {"form":form}
        return render(request, "login.html", context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')