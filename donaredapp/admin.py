from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Item, Zona, Categoria, Profile

# Define an inline admin descriptor for the Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ['movil', 'validado']  # Fields to display
    extra = 0  # Prevents extra empty forms from showing

# Extend the UserAdmin to include the Profile inline
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'categoria', 'usuario', 'activo', 'latitude', 'longitude')
    list_filter = ('zona', 'categoria', 'activo')
    search_fields = ('nombre', 'descripcion', 'direccion')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'zona', 'categoria', 'usuario', 'activo')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'latitude', 'longitude')
        }),
        ('Multimedia', {
            'fields': ('imagen',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion',)
        }),
    )

# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Zona)
admin.site.register(Categoria)
