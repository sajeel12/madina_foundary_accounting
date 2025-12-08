from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'date', 'category', 'description')
    list_filter = ('type', 'date', 'category')
    search_fields = ('description', 'amount')
    date_hierarchy = 'date'
