from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'country', 'is_staff', 'is_active', )
    list_filter = ('is_staff', 'is_active', 'country', )
    search_fields = ('email', 'phone_number', 'country', )
    ordering = ('email',)
