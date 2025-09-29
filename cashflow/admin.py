from django.contrib import admin
from .models import Type, Status, Category, SubCategory, CashFlow

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'status', 'category', 'subcategory', 'amount', 'comment']
    list_filter = ['type', 'status', 'category', 'subcategory']
    date_hierarchy = 'date'
    search_fields = ['category','comment']