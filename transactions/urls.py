from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('categories/', views.categories_list, name='categories_list'),
    path('budgets/', views.budgets_list, name='budgets_list'),
    path('budgets/<int:pk>/', views.budget_detail, name='budget_detail'),
    path('summary/', views.summary_view, name='summary'),
]
