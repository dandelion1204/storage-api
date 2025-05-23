from django.contrib import admin
from core import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
#admin.site.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','name']
    fieldsets = (
        (   None,
            {
                'fields':(
                    'email',
                    'password',
                )}),
        (
            _('Permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields':(
                    'last_login',
                )}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes':(
                    'wide',
                ),
                'fields':(
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
    )


class ProductIngredientAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredient', 'quantity', 'unit')

class IngredientLotAdmin(admin.ModelAdmin):
    list_display = ('ingredient','lot', 'quantity')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Product)
admin.site.register(models.Ingredient)
admin.site.register(models.ProductIngredients, ProductIngredientAdmin)
admin.site.register(models.IngredientLot, IngredientLotAdmin)
