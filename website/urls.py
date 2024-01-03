# urls.py
from django.urls import path
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update/<int:pk>', views.update_record, name='update_record'),
    path('custom_login/', CustomLoginView.as_view(), name='custom_login'),
    path('search/', views.search, name='search'),

]
