"""AI Engine - Spending Predictor using Linear Regression."""

import statistics
import datetime
from django.db.models import Sum
from django.utils import timezone


def _linear_regression(x_values, y_values):
    """Simple least-squares linear regression. Returns (slope, intercept)."""
    n = len(x_values)
    if n < 2:
        return 0, y_values[0] if y_values else 0

    mean_x = statistics.mean(x_values)
    mean_y = statistics.mean(y_values)

    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    denominator = sum((x - mean_x) ** 2 for x in x_values)

    slope = numerator / denominator if denominator != 0 else 0
    intercept = mean_y - slope * mean_x

    return slope, intercept


def predict_next_month():
    """
    Predict spending for the next month per category.

    Uses the last 6 months of data and linear regression.
    Returns a list of dicts with category, predicted_amount, confidence_score.
    """
    from transactions.models import Transaction, Category
    from django.db.models import Sum

    now = timezone.now().date()
    predictions = []

    categories = Category.objects.filter(category_type='expense')

    for category in categories:
        monthly_data = []

        for i in range(5, -1, -1):  # last 6 months
            d = now.replace(day=1) - datetime.timedelta(days=i * 28)
            d = d.replace(day=1)
            total = Transaction.objects.filter(
                category=category,
                date__year=d.year,
                date__month=d.month,
                transaction_type='expense',
            ).aggregate(total=Sum('amount'))['total']
            monthly_data.append(float(total or 0))

        # Only predict if there's at least 1 non-zero month
        non_zero = [v for v in monthly_data if v > 0]
        if not non_zero:
            continue

        x_values = list(range(len(monthly_data)))
        slope, intercept = _linear_regression(x_values, monthly_data)

        # Predict for next month (index 6)
        predicted = max(0, slope * 6 + intercept)

        # Confidence: based on data density (how many of 6 months have data)
        confidence = len(non_zero) / 6

        predictions.append({
            'category': category.name,
            'icon': category.icon,
            'color': category.color,
            'predicted_amount': round(predicted, 2),
            'confidence_score': round(confidence, 2),
            'historical_avg': round(statistics.mean(monthly_data), 2),
            'trend': 'up' if slope > 0 else ('down' if slope < 0 else 'stable'),
        })

    # Sort by predicted amount desc
    predictions.sort(key=lambda x: x['predicted_amount'], reverse=True)

    return predictions
