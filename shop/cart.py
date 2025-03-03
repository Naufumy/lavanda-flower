from decimal import Decimal 
from django.conf import settings 
from shop.models import Flower 

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {} 
        self.cart = cart

    def add(self, flower, quantity=1, update_quantity=False):
        """
        Добавляет товар в корзину или обновляет его количество.
        """
        flower_id = str(flower.id)
        if flower_id not in self.cart:
            self.cart[flower_id] = {'quantity': 0, 'price': str(flower.price)}
        
        if update_quantity:
            self.cart[flower_id]['quantity'] = quantity
        else:
            self.cart[flower_id]['quantity'] += quantity
        
        self.save()

    def remove(self, flower):
        """
        Удаляет товар из корзины.
        """
        flower_id = str(flower.id)
        if flower_id in self.cart:
            del self.cart[flower_id]
            self.save()

    def __iter__(self):
        """
        Перебираем товары в корзине и добавляем данные о цене.
        """
        flower_ids = self.cart.keys()
        flowers = Flower.objects.filter(id__in=flower_ids)

        for flower in flowers:
            self.cart[str(flower.id)]['flower'] = flower
            self.cart[str(flower.id)]['total_price'] = float(self.cart[str(flower.id)]['price']) * self.cart[str(flower.id)]['quantity']
            yield self.cart[str(flower.id)]

    def save(self):
        """Сохраняет изменения в сессии"""
        self.session.modified = True

    def get_total_price(self):
        """Возвращает общую стоимость товаров в корзине"""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    
    def __iter__(self):
        """
        Перебираем товары в корзине и получаем объекты товаров.
        """
        flower_ids = self.cart.keys()
        flowers = Flower.objects.filter(id__in=flower_ids)

        for flower in flowers:
            self.cart[str(flower.id)]['flower'] = flower

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчёт количества товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Получить общую стоимость товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Очистить корзину.
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

        