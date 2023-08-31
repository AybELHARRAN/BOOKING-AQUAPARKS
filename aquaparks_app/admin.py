from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    # Include all the fields you want to display when editing a user
    fields = ('username', 'email', 'user_type', 'gender', 'first_name', 'last_name')
    
    # Specify the fields that appear when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'gender', 'first_name', 'last_name'),
        }),
    )
    fieldsets = None
    list_display = ('username', 'first_name','last_name', 'gender', 'user_type')
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    ...
@admin.register(Conjointe)
class ConjointeAdmin(admin.ModelAdmin):
    ...
@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    ...
'''@admin.register(DinoLand)
class DinoLandAdmin(admin.ModelAdmin):
    ...
@admin.register(Tamaris)
class TamarisAdmin(admin.ModelAdmin):
    ...
@admin.register(AquaFun)
class AquaFunAdmin(admin.ModelAdmin):
    ...
@admin.register(AquaMirage)
class AquaMirageAdmin(admin.ModelAdmin):
    ...'''