"""Management command to seed the database with sample data."""

import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from transactions.models import Category, Transaction, Budget


SAMPLE_TRANSACTIONS = [
    # Income
    ('Salary - March', 80000, 'income', 'Salary & Income', -1),
    ('Freelance project payment', 15000, 'income', 'Salary & Income', -5),
    ('Dividend from mutual fund', 2500, 'income', 'Banking & Finance', -10),

    # Food
    ('Swiggy - Lunch order', 450, 'expense', 'Food & Dining', -1),
    ('Zomato - Dinner', 620, 'expense', 'Food & Dining', -3),
    ('Big Basket grocery', 3200, 'expense', 'Food & Dining', -7),
    ('Starbucks coffee', 380, 'expense', 'Food & Dining', -9),
    ('Dominos pizza night', 750, 'expense', 'Food & Dining', -15),

    # Transport
    ('Ola cab to office', 220, 'expense', 'Transportation', -2),
    ('Petrol refill', 2500, 'expense', 'Transportation', -6),
    ('BMTC monthly pass', 800, 'expense', 'Transportation', -1),

    # Shopping
    ('Amazon - headphones', 3499, 'expense', 'Shopping', -4),
    ('Myntra - winter jacket', 2200, 'expense', 'Shopping', -8),

    # Entertainment
    ('Netflix subscription', 499, 'expense', 'Entertainment', -1),
    ('Movie tickets - PVR', 700, 'expense', 'Entertainment', -12),
    ('Spotify Premium', 119, 'expense', 'Entertainment', -1),

    # Health
    ('Apollo pharmacy', 850, 'expense', 'Health & Medical', -5),
    ('Gym membership - March', 1500, 'expense', 'Health & Medical', -1),

    # Utilities
    ('Electricity bill', 1800, 'expense', 'Housing & Utilities', -3),
    ('Airtel broadband', 999, 'expense', 'Housing & Utilities', -5),
    ('Rent - March', 18000, 'expense', 'Housing & Utilities', -1),

    # Previous month (income)
    ('Salary - February', 80000, 'income', 'Salary & Income', -30),
    ('Freelance design work', 8000, 'income', 'Salary & Income', -35),

    # Previous month (expenses)
    ('Swiggy - Weekend dinner', 980, 'expense', 'Food & Dining', -28),
    ('Grocery - D-Mart', 2700, 'expense', 'Food & Dining', -25),
    ('Uber premium cab', 650, 'expense', 'Transportation', -22),
    ('Amazon - books', 1200, 'expense', 'Shopping', -20),
    ('Hotstar subscription', 299, 'expense', 'Entertainment', -30),
    ('Rent - February', 18000, 'expense', 'Housing & Utilities', -30),
    ('Electricity bill Feb', 1600, 'expense', 'Housing & Utilities', -28),
]


class Command(BaseCommand):
    help = 'Seed the database with sample finance data'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Create categories
        from ai_engine.categorizer import CATEGORY_RULES
        for name, data in CATEGORY_RULES.items():
            cat_type = 'income' if name in ('Salary & Income',) else 'expense'
            Category.objects.get_or_create(
                name=name,
                defaults={'icon': data['icon'], 'color': data['color'], 'category_type': cat_type}
            )

        self.stdout.write(f'  ✅ {Category.objects.count()} categories created')

        # Create transactions
        today = date.today()
        tx_count = 0
        for desc, amount, tx_type, cat_name, day_offset in SAMPLE_TRANSACTIONS:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            tx_date = today + timedelta(days=day_offset)
            Transaction.objects.get_or_create(
                description=desc,
                date=tx_date,
                defaults={
                    'amount': amount,
                    'transaction_type': tx_type,
                    'category': cat,
                    'ai_suggested_category': cat_name,
                }
            )
            tx_count += 1

        self.stdout.write(f'  ✅ {tx_count} transactions created')

        # Create budgets for current month
        budgets_data = [
            ('Food & Dining', 8000),
            ('Transportation', 4000),
            ('Shopping', 5000),
            ('Entertainment', 2000),
            ('Health & Medical', 3000),
            ('Housing & Utilities', 22000),
        ]
        for cat_name, limit in budgets_data:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            Budget.objects.get_or_create(
                category=cat, month=today.month, year=today.year,
                defaults={'monthly_limit': limit}
            )

        self.stdout.write(f'  ✅ {len(budgets_data)} budgets created')
        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write('  → Open http://127.0.0.1:8000/ to view your Finance Tracker')
