# listing/cart.py

from decimal import Decimal
from django.conf import settings
# CHANGED: Import your actual model
from .models import ProductListing

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        # CHANGED: Get ProductListing objects
        products = ProductListing.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            # This will work since your model has a `price` attribute
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_delivery_fee(self):
        return Decimal('50.00') if self.get_subtotal_price() > 0 else 0

    def get_discount(self):
        return Decimal('50.00') if self.get_subtotal_price() >= 500 else 0

    def get_total_price(self):
        return self.get_subtotal_price() + self.get_delivery_fee() - self.get_discount()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()