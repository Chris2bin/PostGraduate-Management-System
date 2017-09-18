from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Field, Area
# from .forms import CategoryFieldForm

class ProfileAdmin(admin.ModelAdmin):
    # form = CategoryFieldForm
    list_filter = ('user_type', 'stud_type')
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Field)
admin.site.register(Area)
admin.site.unregister(Group)