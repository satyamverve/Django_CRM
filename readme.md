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


{% extends "base.html" %}
{% block content %}
 <Center>
        {% if searched %}
            <h1>You Searched For {{ searched }}</h1>
            <br/>
            {% for record in records %}
                {{record}}<br/>
            {% endfor %}
        {% else %}
            <h1>You forgot to search Records...</h1>
        {% endif %}
</Center>
<div class="col-md-0 offset-md-"1>

    
{% if user.is_authenticated %}
<div class="container">
    <div class="row justify-content-end mt-2">
        <div class="col-md-3"> <!-- Adjust the column size as needed -->
            {% if user.is_authenticated %}
            <div class="input-group">
                <span class="input-group-prepend">  
                </span>
                <input class="form-control py-2 border-left-0 border" type="search" placeholder="Search" id="example-search-input" />
                <span class="input-group-append">
                    <button class="btn btn-outline-secondary border-left-0 border" type="button">
                        Search
                    </button>
                </span>
            </div>
            {% endif %}
        </div>
    </div>

    


<table class="table table-striped table-hover table-bordered">
    <thead class= "table-dark">
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Name</th>
        <th scope="col">Email</th>
        <th scope="col">Phone</th>  
        <th scope="col">City</th>
        <th scope="col">State</th>
        <th scope="col">Zip Code</th>
        <th scope="col">Created At</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
{% if records %}
   {% for record in records %}
   
   <tr> {% comment %} this tag is for craeting row {% endcomment %}
       <td><a href="{% url "record" record.id  %}">{{record.id}}</a></td>
      <td>{{record.first_name}} {% comment %} td tag used to create virtual rows {% endcomment %}
      {{record.last_name}}</td>
      <td>{{record.email}}</td>
      <td>{{record.phone}}</td>
      <td>{{record.city}}</td>
      <td>{{record.state}}</td>
      <td>{{record.zip_code}}</td>
      <td>{{record.created_at}}</td>
      <td>
        {% if perms.website.delete_record %}
            <a href="#" class="btn btn-danger" onclick="confirmDelete('{{ record.id }}')">Delete</a>
        {% endif %}
    </td>
</tr>
{% endfor %}
{% endif %}
</tbody>
</table>

<script>
function confirmDelete(recordId) {
var confirmMessage = "Are you sure you want to delete this record?";
if (confirm(confirmMessage)) {
 window.location.href = "{% url 'delete_record' 0 %}".replace('0', recordId);
}
}
</script>

{% else %}

<h1>Login</h1>
</br>
<form method= 'POST' action= "{% url "login" %}" >
    {% csrf_token %}
    <div class="mb-3">
        <input type="text" class="form-control" name='username' placeholder='username' required>
    </div>
    <div class="mb-3">
        <input type="password" class="form-control" name='password' placeholder='password' required>
    </div>
    </br>    
    <button type="submit" class="btn btn-secondary">login</button> 
</form>
{% endif %}
{% endblock %}















{% extends "base.html" %}
{% load custom_filters %}
{% block content %}

<div class="col-md-0 offset-md-0">

    
{% if user.is_authenticated %}
<div class="container">
    <div class="row justify-content-end align-items-center mt-2">
        <div class="col-md-2 text-right">
            {% if perms.website.add_record %}
                <a class="btn btn-primary mr-4" href="{% url 'add_record' %}">Add Record</a>
            {% endif %} 
        </div>
        <div class="col-md-3 text-right">
            {% if user.is_authenticated %}
                <form class="d-inline-flex" method="GET" action="{% url 'home' %}">
                    {% csrf_token %}
                    <input class="form-control py-2 border-left-0 border" type="search" placeholder="Search" aria-label="Search" name="searched">
                    <button class="btn btn-outline-secondary" type="submit">Search</button>
                </form>
            {% endif %}
        </div>
    </div>
    <br/>

    {% if searched %}
        <br/>
        <table class="table table-striped table-hover table-bordered">
            <thead class="table-dark">
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Phone</th>
                    <th scope="col">City</th>
                    <th scope="col">State</th>  
                    <th scope="col">Zip Code</th>
                    <th scope="col">Created At</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                {% for record in records %}
                    <tr>
                        <td><a href="{% url 'record' record.id %}">{{ record.id }}</a></td>
                        <td>
                            {% for word in record.first_name.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                            {% if record.last_name == searched %}
                                <strong>{{ record.last_name }}</strong>
                            {% else %}
                                {{ record.last_name }}
                            {% endif %}
                        </td>
                        <td>
                            {% for word in record.email.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                        </td>
                        <td>
                            {% for word in record.phone.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                        </td>
                        <td>
                            {% for word in record.city.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                        </td>
                        <td>
                            {% for word in record.state.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                        </td>
                        <td>
                            {% for word in record.zip_code.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                        </td>
                        <td>
                            {% for word in record.created_at.split %}
                                {% if word == searched %}
                                    <strong>{{ word }}</strong>
                                {% else %}
                                    {{ word }}
                                {% endif %}
                            {% endfor %}
                        </td>
                        <td>
                            {% if perms.website.delete_record %}
                                <a href="#" class="btn btn-danger" onclick="confirmDelete('{{ record.id }}')">Delete</a>
                            {% endif %}
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <table class="table table-striped table-hover table-bordered">
            <thead class="table-dark">
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Phone</th>
                    <th scope="col">City</th>
                    <th scope="col">State</th>
                    <th scope="col">Zip Code</th>
                    <th scope="col">Created At</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                {% for record in records %}
                    <tr>
                        <td><a href="{% url 'record' record.id %}">{{ record.id }}</a></td>
                        <td>
                            {{ record.first_name }} {{ record.last_name }}
                        </td>
                        <td>{{ record.email }}</td>
                        <td>{{ record.phone }}</td>
                        <td>{{ record.city }}</td>
                        <td>{{ record.state }}</td>
                        <td>{{ record.zip_code }}</td>
                        <td>{{ record.created_at }}</td>
                        <td>
                            {% if perms.website.delete_record %}
                                <a href="#" class="btn btn-danger" onclick="confirmDelete('{{ record.id }}')">Delete</a>
                            {% endif %}
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}

    <script>
        function confirmDelete(recordId) {
            var confirmMessage = "Are you sure you want to delete this record?";
            if (confirm(confirmMessage)) {
                window.location.href = "{% url 'delete_record' 0 %}".replace('0', recordId);
            }
        }
    </script>

{% else %}

<h1>Login</h1>
</br>
<form method="POST" action="{% url 'login' %}">
    {% csrf_token %}
    <div class="mb-3">
        <input type="text" class="form-control" name="username" placeholder="username" required>
    </div>
    <div class="mb-3">
        <input type="password" class="form-control" name="password" placeholder="password" required>
    </div>
    </br>    
    <button type="submit" class="btn btn-secondary">login</button> 
</form>
{% endif %}
{% endblock %}
