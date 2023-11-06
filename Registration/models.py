from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission




class MyRegistrationManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None): 
        if not email:
            raise ValueError('user must have email address')
        
        if not username:
            raise ValueError('user must have user name')
        
        user = self.model( # here value initilize to new user 
                        email = self.normalize_email(email),#this self.normalize_email(email) show email is proper format 
                        username = username,
                        first_name = first_name,
                        last_name = last_name,

        )
        

        user.set_password(password)#automatically hashes the password for security. This ensures that the user's password is stored securely in the database.
        user.is_active = True
        user.save(using = self._db)# save user to default database
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user =  self.create_user(
                        email = self.normalize_email(email),
                        username = username,
                        password= password,
                        first_name = first_name,
                        last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        
        user.save(using = self._db)# save user to default database
        
        


class Registation(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=100)
    
    date_join = models.DateTimeField(auto_now_add=True)
    last_login =models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    # if i defne password field in the model that he save passwored as a plain text so to avoid palan text we define as a sapareate
    USERNAME_FIELD = 'email'      # this line show unique email address
    REQUIRED_FIELDS = ['username','first_name', 'last_name']# this line show required this filed at the time user creation

    objects = MyRegistrationManager()

   

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj = None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
# Create your models here.
