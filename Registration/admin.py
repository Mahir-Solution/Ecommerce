from django.contrib import admin
from .models import Registation
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'password','phone_number']

admin.site.register(Registation,RegistrationAdmin)
# Register your models here.
