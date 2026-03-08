from django.urls import path
from . import views

urlpatterns = [
    path('categorize/', views.categorize_view, name='ai_categorize'),
    path('predict/', views.predict_view, name='ai_predict'),
    path('insights/', views.insights_view, name='ai_insights'),
    path('advisor/', views.advisor_view, name='ai_advisor'),
    path('dashboard/', views.dashboard_view, name='ai_dashboard'),
]
