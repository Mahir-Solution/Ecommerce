from django.contrib import admin
from .models import Category_Model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['catname','slug','catimage','description']
    prepopulated_fields = {'slug': ('catname',) }# is always dictionary slug is key and you want which field is type the slug name is automate type
admin.site.register(Category_Model,CategoryAdmin)
# Register your models here.
