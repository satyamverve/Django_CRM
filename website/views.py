from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('home')
    else:
        # If the request method is not POST or the authentication failed, render the form again
        form = AuthenticationForm()
        return render(request, 'home.html', {'form': form}) #passing the form coz when we go to home page then we can do something with the input fields


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')
    
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password) #why password not password1!!, coz we took password1 and signed it to variable called password
            login(request, user)
            messages.success(request, "You have successfully register")
            return redirect('home')
    else:
        form= SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})