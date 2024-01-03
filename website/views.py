# views.py

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse

from django.db.models import Q

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '').strip()
        if searched:
            items = ['first_name', 'last_name','email', 'phone', 'city', 'state', 'zip_code', 'created_at']
            query = Q()
            for item in items:
                query |= Q(**{f'{item}__icontains': searched})
            records = Record.objects.filter(query)
            if records:
                return render(request, 'home.html', {'searched': searched, 'records': records})
            else:
                messages.info(request, "No records found for the searched item.")
        else:
            messages.warning(request, "Please enter a search term.")
    return render(request, 'home.html', {})



class CustomLoginView(LoginView):
    template_name = 'home.html'

    def get_success_url(self):
        # Redirect to the next parameter if available, otherwise to a default URL
        return self.request.GET.get('next', '/')


@csrf_protect
@permission_required('website.view_record',login_url='/custom_login/')
def home(request):
    searched = request.GET.get('searched', '')
    items = ['first_name', 'last_name', 'email', 'phone', 'city', 'state', 'zip_code', 'created_at']

    if searched:
        query = Q()
        for item in items:
            query |= Q(**{f'{item}__icontains': searched})
        records = Record.objects.filter(query)
        if records:
            return render(request, 'home.html', {'searched': searched, 'records': records})
        else:
            messages.info(request, "No records found for the searched item.")
    else:
        records = Record.objects.all()
        

    user = request.user
    return render(request, 'home.html', {'records': records, 'user': user, 'searched': searched})



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
            messages.error(request, "Oops! It seems like the credentials provided are invalid, or your account is pending for approval by the admin. Please be patient and try logging in again. If you're awaiting approval, our admin will get to it as soon as possible. Thank you for your understanding!")

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
            # group=Group.objects.get(name='Editor')
            # user.groups.add(group)
            #Authenticate and login
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # user = authenticate(request, username=username, password=password) #why password not password1!!, coz we took password1 and signed it to variable called password
            # login(request, user)
            messages.success(request, "You have successfully registered, wait for admin approval before login..")
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
@permission_required('website.delete_record',login_url='/custom_login/')  
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
@permission_required('website.add_record', login_url='/custom_login/')
def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully...")
                return redirect('home')

        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in...!!!")
        return redirect('home')

@csrf_protect
@permission_required('website.change_record',login_url='/custom_login/')  
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record= Record.objects.get(id=pk)
        form= AddRecordForm(request.POST or None, instance= current_record)
        if form.is_valid():
            update_record=form.save()
            messages.success(request, "Record Updated Successfully...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request,"You must be logged In...!!!")
        return redirect('home')