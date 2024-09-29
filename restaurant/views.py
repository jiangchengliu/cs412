from django.shortcuts import render
from django.http import HttpResponse
import random
import time 
from datetime import datetime, timedelta

# Create your views here.

MENU_ITEMS = {
    "Spicy Miso Pork Donburi": 15.00,
    "Takoyaki": 9.00,
    "Seaweed Salad": 7.00,
    "Niku Udon": 22.00,
}

DAILY_SPECIALS = [
    {'name': 'Sukiyaki Don', 'price': 24.00},
    {'name': 'Kani Ankake', 'price': 25.00},
    {'name': 'Beef Truffle Udon', 'price': 22.00},
    {'name': 'Cold Mentaiko Udon', 'price': 25.00},
]


def main(request):
    return render(request, "restaurant/main.html")

def order(request):
    daily_special = random.choice(DAILY_SPECIALS)
    context = {
        "menu_items": MENU_ITEMS,
        "daily_special": daily_special,
    }
    return render(request, "restaurant/order.html", context)

def confirmation(request):
    
    current_time = datetime.now()
    
    rand = random.randint(30, 60)

    ready_time = current_time + timedelta(minutes=rand)
    
    ordered_items = []
    total = 0
    ordered = False
    extra = ""
    if request.method == "POST":
        ordered = True
        for item, price in MENU_ITEMS.items():
            if item in request.POST:
                ordered_items.append({"name": item, "price": price})
                total += price
        if "daily_special" in request.POST:
            ordered_items.append({"name": request.POST["special_name"], "price": request.POST["special_price"]})
            total += float(request.POST["special_price"])
    
    if request.POST.get('Extra Meat'):
            total += 3.00
            extra = 'Extra Meat'
        
    customer_name = request.POST.get('customer_name')
    customer_phone = request.POST.get('customer_phone')
    customer_email = request.POST.get('customer_email')

        # Add special instructions if any
    special_instructions = request.POST.get('special_instructions', '')
    

        # Context for confirmation page
    context = {
        'ordered_items': ordered_items,
        'total_price': total,
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'customer_email': customer_email,
        'special_instructions': special_instructions,
        'ordered': ordered,
        'extra': extra,
        'ready': ready_time
    }
    print(context)

    return render(request, 'restaurant/confirmation.html', context)

    

