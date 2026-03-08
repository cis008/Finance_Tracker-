from django.urls import path
from . import views

urlpatterns = [
    path('monthly/', views.monthly_trend_view, name='monthly_trend'),
    path('breakdown/', views.category_breakdown_view, name='category_breakdown'),
]
