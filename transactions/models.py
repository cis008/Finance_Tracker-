from django.db import models
from django.utils import timezone


class Category(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, default='💰')
    color = models.CharField(max_length=20, default='#6366f1')
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=EXPENSE)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=EXPENSE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions'
    )
    ai_suggested_category = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} - ₹{self.amount}"


class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['category', 'month', 'year']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.category.name} Budget - {self.month}/{self.year}"


class SpendingPrediction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='predictions')
    predicted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['category', 'month', 'year']

    def __str__(self):
        return f"{self.category.name} Prediction - {self.month}/{self.year}"
