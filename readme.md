# Commands
1. Run Server:
python3 manage.py runserver

2. Make Migrations after updating Models and forms
python3 manage.py makemigrations

3. Migrate the data to Database after making migrations
python3 manage.py migrate

4. Create Super User
python3 manage.py createsuperuser

5. Run on local server:
[5.1] Update your settings.py file
ALLOWED_HOSTS = ['Local_IP', 'localhost', '127.0.0.1','*']
> update Local_IP with your own

[5.2] Run this command in other Systems to show your application:
http://Local_Ip:8000





# Django Admin Permisions:
From this we can make groups or individual also to give the permission of add, delete, change/update and view the app

{% if perms.website.delete_record %}

{% endif %}


perms.app_name.operation_model_name
{% if perms.website.add_record %}
here, operation = add, delete, change/update, view

and in this application we have model call Record
remember that always use all the name with perms in lowercase

# Django Permissions
NOTE: Bydefault django app have all the permissions
for giving custom django permissions to views need to follow these steps

1. Import Permission Required
from django.contrib.auth.decorators import permission_required

2. Make a login View to prevent the NOT FOUND error
class CustomLoginView(LoginView):
    template_name = 'home.html' #give html file where you want to redirect after login

    def get_success_url(self):
        # Redirect to the next parameter if available, otherwise to a default URL
        return self.request.GET.get('next', '/')

3. Update the "urls.py" file of your app
from .views import CustomLoginView

>Now, add this path i.e., 
path('login/', CustomLoginView.as_view(), name='login'),


4. Use the decoratotors which you imported "@permission_required" for giving custom views permissions in "views.py" file

>i.e, @permission_required('app_name.view_my_model', login_url='/login/')

> Replace app_name with your application app_name
> Replace my_model with your "model.py" class name in lower_case

## Let's get started the permission required for views
> make sure to import "from django.contrib.auth.decorators import permission_required" in "views.py" file before proceeding 

1. View (Read) Operation:
@permission_required('app_name.view_my_model', login_url='/login/')
Ex;
> @permission_required('website.view_record',login_url='/login/')

2. Edit (Update) Operation:
@permission_required('website.change_record',login_url='/login/')  
Ex;
> @permission_required('app_name.delete_my_model', login_url='/login/')

3. Delete Operation
@permission_required('app_name.delete_my_model', login_url='/login/')
Ex;
> @permission_required('website.delete_record',login_url='/login/')  

4. Add (Create) Operation
@permission_required('app_name.delete_my_model', login_url='/login/')
Ex;
@permission_required('website.create_record',login_url='/login/') 

## templatetags
This folder is for adding your custom filters to the features of the App

## staticfiles
Here are some of the examples of static files in Django:
Images, CSS, JavaScript, Fonts, Videos, Audio files.
Overall, static files are an important part of any Django project. By understanding how to use static files, you can improve the performance, scalability, and maintainability of your project.

1. When you add/update the below code in "settings.py" file 
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

2. Then 'staticfiles' folder automatically create after running the below command:
python3 manage.py collectstatic

Note: To update static files run this command

## signals.py
This file is created for make the feature of "group"
i.e, When I add a new user(register) then the new user must be automatically added to some group which will have used for limiting the features by admin control.

> And also withot making signals.py file we can make this feature 
but there is the chances of getting error when this group is not created by the admin in django superadmin but when we use signals.py file then it automatically create the group in by admin side on django superadmin either the group is available or not
