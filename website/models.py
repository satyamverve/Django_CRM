from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User

class Record(models.Model):
    created_at=models.DateField(auto_now_add=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField( max_length=254)
    phone=models.CharField(max_length=12)
    address=models.CharField(max_length=50)
    city=models.CharField( max_length=50)
    state=models.CharField( max_length=50)
    zip_code=models.CharField( max_length=50)
    country = CountryField(default='India')
    

    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
    


    
   
   
   
   
   
   
   
    
    
    




