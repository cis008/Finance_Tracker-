"""Analytics app views."""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ai_engine.analyzer import get_monthly_trend, get_category_breakdown, get_monthly_summary


@require_http_methods(["GET"])
def monthly_trend_view(request):
    months = int(request.GET.get('months', 6))
    trend = get_monthly_trend(months)
    return JsonResponse({'trend': trend})


@require_http_methods(["GET"])
def category_breakdown_view(request):
    from django.utils import timezone
    now = timezone.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))
    breakdown = get_category_breakdown(year, month)
    return JsonResponse({'breakdown': breakdown, 'month': month, 'year': year})
