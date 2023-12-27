from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import User



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
            user=form.save(commit=False)
            user.is_active = False  # Mark the user as inactive until admin approval
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # user = authenticate(request, username=username, password=password) #why password not password1!!, coz we took password1 and signed it to variable called password
            # login(request, user)
            messages.success(request, "You have successfully registered, wait for approval for login...")
            return redirect('home')
    else:
        form= SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form': form})

def admin_approval(request):
    # Check if the user has admin privileges before proceeding
    if request.user.is_authenticated and request.user.is_staff:
        users_to_approve = User.objects.filter(is_active=False)
        return render(request, 'admin_approval.html', {'users_to_approve': users_to_approve})
    else:
        messages.error(request, "You have not approved yet...")
        return redirect('home')


def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look Up Records
        customer_record=Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "Please login first to view the page..")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it= Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Records Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You must be login first..!")
        return redirect('home')
    
def add_record(request):
    form= AddRecordForm(request.POST or None) #None means they want something maybe they want to change something
    if request.user.is_authenticated:
        if request.method =="POST":
            if form.is_valid():
                add_record=form.save()
                messages.success(request, "Record Added Successfully...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request,"You must be logged In...!!!")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record= Record.objects.get(id=pk)
        form= AddRecordForm(request.POST or None, instance= current_record)
        if form.is_valid():
            add_record=form.save()
            messages.success(request, "Record Updated Successfully...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request,"You must be logged In...!!!")
        return redirect('home')



    