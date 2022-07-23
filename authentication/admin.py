from django.contrib import admin
from .models import CustomUser


# Register your models here.
class UserAdmin(admin.ModelAdmin):

    list_display=('username','email','is_staff','first_name','last_name')
    search_fields =('username','email','is_staff')
    list_per_page=25
    

admin.site.register(CustomUser, UserAdmin)
