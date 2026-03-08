from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('transactions.urls')),
    path('api/ai/', include('ai_engine.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('transactions/', TemplateView.as_view(template_name='transactions.html'), name='transactions'),
    path('analytics/', TemplateView.as_view(template_name='analytics.html'), name='analytics'),
    path('budgets/', TemplateView.as_view(template_name='budgets.html'), name='budgets'),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
]
