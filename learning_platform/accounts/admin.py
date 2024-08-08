from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomUser

#admin.site.register(CustomUser, UserAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'name', 'surname', 'user_type']
    fieldsets = UserAdmin.fieldsets + (('Custom fields', {'fields': ('name', 'surname', 'user_type')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Custom fields', {'fields': ('name', 'surname', 'user_type')}),)    


admin.site.register(CustomUser, CustomUserAdmin)