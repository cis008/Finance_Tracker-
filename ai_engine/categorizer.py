"""AI Engine - Expense Categorizer"""

# Keyword-based category rules
CATEGORY_RULES = {
    'Food & Dining': {
        'icon': '🍽️', 'color': '#f59e0b',
        'keywords': [
            'restaurant', 'food', 'grocery', 'groceries', 'pizza', 'burger', 'coffee',
            'cafe', 'swiggy', 'zomato', 'dominos', 'kfc', 'mcdonald', 'starbucks',
            'lunch', 'dinner', 'breakfast', 'meal', 'snack', 'bakery', 'biryani',
            'hotel', 'eat', 'dine', 'fruits', 'vegetables', 'milk', 'eggs',
        ]
    },
    'Transportation': {
        'icon': '🚗', 'color': '#3b82f6',
        'keywords': [
            'uber', 'ola', 'cab', 'taxi', 'bus', 'metro', 'train', 'auto',
            'petrol', 'diesel', 'fuel', 'gas', 'parking', 'toll', 'rapido',
            'flight', 'airline', 'ticket', 'travel', 'transport', 'vehicle',
        ]
    },
    'Shopping': {
        'icon': '🛍️', 'color': '#ec4899',
        'keywords': [
            'amazon', 'flipkart', 'myntra', 'ajio', 'shopping', 'clothes', 'clothing',
            'shoes', 'fashion', 'dress', 'shirt', 'trouser', 'bag', 'accessories',
            'online', 'order', 'purchase', 'buy', 'mall', 'store', 'market',
        ]
    },
    'Entertainment': {
        'icon': '🎬', 'color': '#8b5cf6',
        'keywords': [
            'netflix', 'amazon prime', 'hotstar', 'spotify', 'youtube', 'movie',
            'cinema', 'theatre', 'game', 'gaming', 'subscription', 'streaming',
            'music', 'concert', 'show', 'ticket', 'park', 'amusement',
        ]
    },
    'Health & Medical': {
        'icon': '🏥', 'color': '#10b981',
        'keywords': [
            'doctor', 'hospital', 'clinic', 'medicine', 'pharmacy', 'chemist',
            'medical', 'health', 'gym', 'fitness', 'yoga', 'dentist', 'lab',
            'test', 'checkup', 'diagnosis', 'surgery', 'insurance',
        ]
    },
    'Housing & Utilities': {
        'icon': '🏠', 'color': '#f97316',
        'keywords': [
            'rent', 'electricity', 'water', 'gas', 'internet', 'wifi', 'broadband',
            'maintenance', 'repair', 'plumber', 'electrician', 'society', 'flat',
            'apartment', 'house', 'home', 'furniture', 'appliance',
        ]
    },
    'Education': {
        'icon': '📚', 'color': '#06b6d4',
        'keywords': [
            'school', 'college', 'university', 'course', 'tutorial', 'class',
            'tuition', 'books', 'stationery', 'udemy', 'coursera', 'fee',
            'learning', 'exam', 'certification', 'training',
        ]
    },
    'Salary & Income': {
        'icon': '💼', 'color': '#22c55e',
        'keywords': [
            'salary', 'income', 'wage', 'bonus', 'freelance', 'client',
            'payment received', 'credit', 'deposit', 'transfer received', 'earned',
        ]
    },
    'Banking & Finance': {
        'icon': '🏦', 'color': '#64748b',
        'keywords': [
            'emi', 'loan', 'interest', 'credit card', 'bank', 'investment',
            'mutual fund', 'sip', 'stocks', 'dividend', 'returns', 'fd',
            'lic', 'insurance premium', 'tax',
        ]
    },
    'Personal Care': {
        'icon': '💆', 'color': '#f43f5e',
        'keywords': [
            'salon', 'hair', 'spa', 'beauty', 'cosmetics', 'skincare', 'makeup',
            'parlour', 'barbershop', 'grooming', 'toiletries', 'soap', 'shampoo',
        ]
    },
    'Bills & Subscriptions': {
        'icon': '🧾', 'color': '#0ea5e9',
        'keywords': [
            'bill', 'recharge', 'mobile recharge', 'postpaid', 'prepaid', 'broadband bill',
            'electricity bill', 'water bill', 'gas bill', 'subscription', 'membership',
            'renewal', 'monthly plan', 'ott', 'apple music', 'youtube premium',
        ]
    },
    'Travel & Vacation': {
        'icon': '✈️', 'color': '#14b8a6',
        'keywords': [
            'trip', 'vacation', 'holiday', 'resort', 'hotel booking', 'airbnb',
            'booking.com', 'makemytrip', 'goibibo', 'expedia', 'visa', 'tour',
            'sightseeing', 'luggage', 'travel insurance',
        ]
    },
    'Gifts & Donations': {
        'icon': '🎁', 'color': '#a855f7',
        'keywords': [
            'gift', 'present', 'birthday gift', 'anniversary', 'wedding gift',
            'donation', 'charity', 'ngo', 'temple donation', 'offering', 'fundraiser',
        ]
    },
    'Kids & Family': {
        'icon': '👨‍👩‍👧', 'color': '#f97316',
        'keywords': [
            'kids', 'child', 'baby', 'diapers', 'toys', 'school bus', 'daycare',
            'family', 'parents', 'household', 'family outing', 'baby food',
        ]
    },
    'Pets': {
        'icon': '🐾', 'color': '#84cc16',
        'keywords': [
            'pet', 'dog', 'cat', 'pet food', 'vet', 'veterinary', 'pet clinic',
            'pet grooming', 'pet supplies',
        ]
    },
    'Electronics & Gadgets': {
        'icon': '📱', 'color': '#6366f1',
        'keywords': [
            'mobile', 'phone', 'laptop', 'tablet', 'headphones', 'earbuds', 'charger',
            'keyboard', 'mouse', 'monitor', 'electronics', 'gadget', 'appliances',
            'repair service',
        ]
    },
    'Home Improvement': {
        'icon': '🛠️', 'color': '#f59e0b',
        'keywords': [
            'paint', 'carpenter', 'hardware', 'tool', 'drill', 'renovation',
            'interior', 'decor', 'curtains', 'lighting', 'fixtures', 'home repair',
        ]
    },
    'Taxes & Government': {
        'icon': '🏛️', 'color': '#64748b',
        'keywords': [
            'income tax', 'gst', 'property tax', 'road tax', 'challan', 'fine',
            'government fee', 'passport fee', 'license fee', 'registration fee',
        ]
    },
    'Business Expenses': {
        'icon': '🧑‍💼', 'color': '#0f766e',
        'keywords': [
            'office', 'software', 'saas', 'hosting', 'domain', 'co-working',
            'client meeting', 'business lunch', 'business travel', 'invoice paid',
            'professional fee', 'consultant',
        ]
    },
}


def categorize(description: str) -> dict:
    """
    Categorize a transaction description using keyword matching.

    Returns:
        dict with 'category', 'icon', 'color', 'confidence'
    """
    if not description:
        return {'category': 'Other', 'icon': '📦', 'color': '#94a3b8', 'confidence': 0.0}

    text = description.lower().strip()
    best_match = None
    best_score = 0

    for category_name, data in CATEGORY_RULES.items():
        score = 0
        for keyword in data['keywords']:
            if keyword in text:
                # Longer keyword matches = higher confidence
                score += len(keyword)

        if score > best_score:
            best_score = score
            best_match = (category_name, data['icon'], data['color'])

    if best_match:
        # Normalize confidence: cap at 1.0 for scores >= 10
        confidence = min(1.0, best_score / 10.0)
        return {
            'category': best_match[0],
            'icon': best_match[1],
            'color': best_match[2],
            'confidence': round(confidence, 2),
        }

    return {'category': 'Other', 'icon': '📦', 'color': '#94a3b8', 'confidence': 0.0}
