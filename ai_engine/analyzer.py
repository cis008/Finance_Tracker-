"""AI Engine - Spending Analyzer"""

from django.db.models import Sum, Avg, Count
from django.utils import timezone
import datetime


def get_monthly_summary(year=None, month=None):
    """Returns income/expense totals for a given month."""
    from transactions.models import Transaction

    now = timezone.now()
    year = year or now.year
    month = month or now.month

    qs = Transaction.objects.filter(date__year=year, date__month=month)
    income = qs.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = qs.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    return {
        'year': year,
        'month': month,
        'income': float(income),
        'expense': float(expense),
        'net': float(income) - float(expense),
        'savings_rate': round((float(income) - float(expense)) / float(income) * 100, 1) if income else 0,
    }


def get_category_breakdown(year=None, month=None):
    """Returns expense breakdown by category for a given month."""
    from transactions.models import Transaction

    now = timezone.now()
    year = year or now.year
    month = month or now.month

    data = (
        Transaction.objects
        .filter(date__year=year, date__month=month, transaction_type='expense')
        .values('category__name', 'category__icon', 'category__color')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total')
    )

    result = []
    total_expense = sum(float(r['total']) for r in data)
    for row in data:
        amt = float(row['total'])
        result.append({
            'category': row['category__name'] or 'Uncategorized',
            'icon': row['category__icon'] or '📦',
            'color': row['category__color'] or '#94a3b8',
            'amount': amt,
            'count': row['count'],
            'percentage': round(amt / total_expense * 100, 1) if total_expense else 0,
        })
    return result


def get_monthly_trend(months=6):
    """Returns month-by-month income/expense totals for the last N months."""
    from transactions.models import Transaction

    now = timezone.now().date()
    result = []

    for i in range(months - 1, -1, -1):
        # Go back i months
        d = now.replace(day=1) - datetime.timedelta(days=i * 28)
        # Normalize to first of month
        d = d.replace(day=1)
        y, m = d.year, d.month

        qs = Transaction.objects.filter(date__year=y, date__month=m)
        income = float(qs.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0)
        expense = float(qs.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0)

        result.append({
            'month': d.strftime('%b %Y'),
            'year': y,
            'month_num': m,
            'income': income,
            'expense': expense,
            'net': income - expense,
        })

    return result


def get_ai_insights():
    """Generate plain-language spending insights."""
    from transactions.models import Transaction
    from django.db.models import Sum

    now = timezone.now()
    curr_month = get_monthly_summary(now.year, now.month)

    # Previous month
    prev_d = (now.replace(day=1) - datetime.timedelta(days=1))
    prev_month = get_monthly_summary(prev_d.year, prev_d.month)

    insights = []

    # Spending vs last month
    if prev_month['expense'] > 0:
        change = curr_month['expense'] - prev_month['expense']
        pct = abs(change) / prev_month['expense'] * 100
        if change > 0:
            insights.append(f"⚠️ Your spending is up ₹{abs(change):,.0f} ({pct:.1f}%) compared to last month.")
        elif change < 0:
            insights.append(f"✅ Great job! You spent ₹{abs(change):,.0f} ({pct:.1f}%) less than last month.")
        else:
            insights.append("📊 Your spending is consistent with last month.")

    # Savings rate
    if curr_month['income'] > 0:
        sr = curr_month['savings_rate']
        if sr >= 30:
            insights.append(f"🌟 Excellent savings rate of {sr}% this month!")
        elif sr >= 15:
            insights.append(f"💡 Decent savings rate of {sr}%. Aim for 30% to build wealth faster.")
        elif sr >= 0:
            insights.append(f"⚡ Low savings rate ({sr}%). Consider reviewing your expenses.")
        else:
            insights.append(f"🚨 You're spending more than you earn this month!")

    # Top category
    breakdown = get_category_breakdown(now.year, now.month)
    if breakdown:
        top = breakdown[0]
        insights.append(f"🏆 Top spending category: {top['icon']} {top['category']} (₹{top['amount']:,.0f}, {top['percentage']}% of expenses)")

    if not insights:
        insights.append("📝 Add some transactions to get personalized AI insights!")

    return insights
