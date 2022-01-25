from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse

from .forms import SignUpForm, LoginForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('blogApp:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Congratulations, registered successfully!")
            return redirect('blogApp:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def log_in(request):
    if request.user.is_authenticated:
        return redirect('blogApp:home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # We check if the data is correct
            user = authenticate(email=email, password=password)
            if user:  # If the returned object is not None
                login(request, user)  # we connect the user
                return redirect('blogApp:home')
            else:  # otherwise an error will be displayed
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))