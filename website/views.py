from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

def home(request):
    #making a variable to take everything in the Record
    records= Record.objects.all()
    
    #check to see if user logging in
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            #Authenticate   
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
        return render(request, 'home.html', {'records': records}) 
    
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


def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look Up Records
        customer_record=Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "Please login first to view the page..")
        return redirect('home')
