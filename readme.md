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

