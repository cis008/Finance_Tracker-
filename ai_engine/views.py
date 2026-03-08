"""AI Engine app views — exposes categorization, prediction, and insights via JSON API."""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .categorizer import categorize
from .predictor import predict_next_month
from .analyzer import get_ai_insights, get_monthly_summary, get_category_breakdown, get_monthly_trend
from .anthropic_service import ai_categorize_description, ai_financial_advice


@csrf_exempt
@require_http_methods(["POST"])
def categorize_view(request):
    """POST /api/ai/categorize/ — auto-categorize a transaction description."""
    try:
        data = json.loads(request.body)
        description = data.get('description', '')
    except json.JSONDecodeError:
        description = ''

    ai_result = ai_categorize_description(description)
    result = ai_result or categorize(description)
    result['source'] = 'anthropic' if ai_result else 'rules'
    return JsonResponse(result)


@require_http_methods(["GET"])
def predict_view(request):
    """GET /api/ai/predict/ — return next-month predictions per category."""
    predictions = predict_next_month()
    return JsonResponse({'predictions': predictions})


@require_http_methods(["GET"])
def insights_view(request):
    """GET /api/ai/insights/ — return AI-generated spending insights."""
    insights = get_ai_insights()
    return JsonResponse({'insights': insights})


@require_http_methods(["GET"])
def dashboard_view(request):
    """GET /api/ai/dashboard/ — combined dashboard data."""
    from django.utils import timezone
    now = timezone.now()

    summary = get_monthly_summary(now.year, now.month)
    breakdown = get_category_breakdown(now.year, now.month)
    trend = get_monthly_trend(6)
    insights = get_ai_insights()

    return JsonResponse({
        'summary': summary,
        'category_breakdown': breakdown,
        'trend': trend,
        'insights': insights,
    })


@csrf_exempt
@require_http_methods(["POST"])
def advisor_view(request):
    """POST /api/ai/advisor/ — Anthropic-powered financial advice with fallback."""
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        data = {}

    from django.utils import timezone
    now = timezone.now()
    year = int(data.get('year', now.year))
    month = int(data.get('month', now.month))
    question = (data.get('question') or '').strip()

    summary = get_monthly_summary(year, month)
    breakdown = get_category_breakdown(year, month)
    trend = get_monthly_trend(6)

    advice = ai_financial_advice(question, summary, breakdown, trend)
    if advice:
        return JsonResponse({
            'advice': advice,
            'source': 'anthropic',
            'summary': summary,
        })

    local_insights = get_ai_insights()
    fallback = [
        "Anthropic API is not configured or temporarily unavailable.",
        *local_insights,
    ]
    return JsonResponse({
        'advice': '\n'.join(f"- {line}" for line in fallback),
        'source': 'fallback',
        'summary': summary,
    })
