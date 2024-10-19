from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserAddForm, UserEditForm


# Register your models here.
class BSSBUserAdmin(UserAdmin):
    add_form = UserAddForm
    form = UserEditForm
    model = get_user_model()
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        ('permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'email', 'password1', 'password2',
                'is_active', 'groups', 'user_permissions'
            )
        })
    )
    search_fields = ('email', )
    ordering = ('email', )

admin.site.register(get_user_model(), BSSBUserAdmin)