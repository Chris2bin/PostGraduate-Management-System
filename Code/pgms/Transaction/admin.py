from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('Date_uploaded',)

admin.site.register(Transaction, TransactionAdmin)
