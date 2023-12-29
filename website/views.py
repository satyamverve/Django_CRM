from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group

@csrf_protect
def home(request):
    records = Record.objects.all()
    user=request.user
    return render(request, 'home.html', {'records': records, 'user':user})

@csrf_protect
def login_user(request):
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

    # If the request method is not POST or the authentication failed, render the form again
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@csrf_protect   
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

@csrf_protect   
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Editor')
            user.groups.add(group)
            #Authenticate and login
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # user = authenticate(request, username=username, password=password) #why password not password1!!, coz we took password1 and signed it to variable called password
            # login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('login')
    else:
        form= SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})


@csrf_protect
def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look Up Records
        customer_record=Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "Please login first to view the page..")
        return redirect('home')


@csrf_protect
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it= Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Records Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You must be login first..!")
        return redirect('home')

@csrf_protect   
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

@csrf_protect   
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