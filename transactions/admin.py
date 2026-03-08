from django.contrib import admin
from .models import Category, Transaction, Budget, SpendingPrediction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'category_type', 'color']
    list_filter = ['category_type']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'transaction_type', 'category', 'date']
    list_filter = ['transaction_type', 'category', 'date']
    search_fields = ['description', 'notes']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'monthly_limit', 'month', 'year']
    list_filter = ['year', 'month']


@admin.register(SpendingPrediction)
class SpendingPredictionAdmin(admin.ModelAdmin):
    list_display = ['category', 'predicted_amount', 'confidence_score', 'month', 'year']
