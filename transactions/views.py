"""Transactions app views — full CRUD + dashboard APIs."""

import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Transaction, Category, Budget


# ── Helpers ──────────────────────────────────────────────────────────────────

def transaction_to_dict(t):
    return {
        'id': t.id,
        'amount': float(t.amount),
        'description': t.description,
        'date': str(t.date),
        'transaction_type': t.transaction_type,
        'category_id': t.category_id,
        'category_name': t.category.name if t.category else 'Uncategorized',
        'category_icon': t.category.icon if t.category else '📦',
        'category_color': t.category.color if t.category else '#94a3b8',
        'ai_suggested_category': t.ai_suggested_category,
        'notes': t.notes,
        'created_at': t.created_at.isoformat(),
    }


def category_to_dict(c):
    return {
        'id': c.id,
        'name': c.name,
        'icon': c.icon,
        'color': c.color,
        'category_type': c.category_type,
    }


def budget_to_dict(b, actual=0):
    limit = float(b.monthly_limit)
    return {
        'id': b.id,
        'category_id': b.category_id,
        'category_name': b.category.name,
        'category_icon': b.category.icon,
        'category_color': b.category.color,
        'monthly_limit': limit,
        'month': b.month,
        'year': b.year,
        'actual': actual,
        'percentage': round(actual / limit * 100, 1) if limit else 0,
        'status': 'over' if actual > limit else ('warning' if actual > limit * 0.8 else 'ok'),
    }


# ── Transaction endpoints ─────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def transactions_list(request):
    if request.method == "GET":
        qs = Transaction.objects.select_related('category').all()

        # Filters
        t_type = request.GET.get('type')
        category_id = request.GET.get('category')
        month = request.GET.get('month')
        year = request.GET.get('year')
        search = request.GET.get('search')

        if t_type:
            qs = qs.filter(transaction_type=t_type)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if month:
            qs = qs.filter(date__month=month)
        if year:
            qs = qs.filter(date__year=year)
        if search:
            qs = qs.filter(description__icontains=search)

        return JsonResponse({'transactions': [transaction_to_dict(t) for t in qs[:200]]})

    # POST
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Auto-categorize if no category provided
    from ai_engine.categorizer import categorize
    ai_result = categorize(data.get('description', ''))

    category = None
    cat_name = data.get('category_name') or ai_result['category']
    if cat_name:
        category, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={
                'icon': ai_result['icon'],
                'color': ai_result['color'],
                'category_type': data.get('transaction_type', 'expense'),
            }
        )

    t = Transaction.objects.create(
        amount=data.get('amount', 0),
        description=data.get('description', ''),
        date=data.get('date', str(timezone.now().date())),
        transaction_type=data.get('transaction_type', 'expense'),
        category=category,
        ai_suggested_category=ai_result['category'],
        notes=data.get('notes', ''),
    )
    return JsonResponse(transaction_to_dict(t), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def transaction_detail(request, pk):
    try:
        t = Transaction.objects.select_related('category').get(pk=pk)
    except Transaction.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == "GET":
        return JsonResponse(transaction_to_dict(t))

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        for field in ['amount', 'description', 'date', 'transaction_type', 'notes']:
            if field in data:
                setattr(t, field, data[field])

        if 'category_name' in data:
            cat, _ = Category.objects.get_or_create(name=data['category_name'])
            t.category = cat

        t.save()
        return JsonResponse(transaction_to_dict(t))

    # DELETE
    t.delete()
    return JsonResponse({'success': True})


# ── Category endpoints ────────────────────────────────────────────────────────

@require_http_methods(["GET"])
def categories_list(request):
    cats = Category.objects.all()
    return JsonResponse({'categories': [category_to_dict(c) for c in cats]})


# ── Budget endpoints ──────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def budgets_list(request):
    now = timezone.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))

    if request.method == "GET":
        budgets = Budget.objects.filter(month=month, year=year).select_related('category')
        result = []
        for b in budgets:
            actual = float(
                Transaction.objects.filter(
                    category=b.category, date__month=month, date__year=year,
                    transaction_type='expense'
                ).aggregate(total=Sum('amount'))['total'] or 0
            )
            result.append(budget_to_dict(b, actual))
        return JsonResponse({'budgets': result, 'month': month, 'year': year})

    # POST
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    cat, _ = Category.objects.get_or_create(name=data.get('category_name', 'Other'))
    b, created = Budget.objects.update_or_create(
        category=cat,
        month=data.get('month', now.month),
        year=data.get('year', now.year),
        defaults={'monthly_limit': data.get('monthly_limit', 0)},
    )
    return JsonResponse(budget_to_dict(b), status=201 if created else 200)


@csrf_exempt
@require_http_methods(["DELETE"])
def budget_detail(request, pk):
    try:
        Budget.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Budget.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


# ── Summary endpoint ──────────────────────────────────────────────────────────

@require_http_methods(["GET"])
def summary_view(request):
    now = timezone.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))

    qs = Transaction.objects.filter(date__year=year, date__month=month)
    income = float(qs.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0)
    expense = float(qs.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0)
    count = qs.count()

    return JsonResponse({
        'income': income,
        'expense': expense,
        'net': income - expense,
        'count': count,
        'savings_rate': round((income - expense) / income * 100, 1) if income else 0,
        'month': month,
        'year': year,
    })
