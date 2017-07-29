from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user_type',)
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)