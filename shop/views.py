from shop.models import Flower, PromotionPage
from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from .forms import CartAddFlowerForm,  OrderCreateForm
from .models import OrderItem, PromotionPage
from .telegram_bot import send_telegram_message
from django.db import models
from django.shortcuts import render, get_object_or_404

def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'shop/flower_list.html', {'flowers': flowers})

def flower_detail(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    form = CartAddFlowerForm()
    return render(request, 'shop/flower/detail.html', {'flower': flower, 'form': form})

def cart_add(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)

    form = CartAddFlowerForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(flower=flower, quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('cart_detail')

def cart_remove(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)
    cart.remove(flower)
    return redirect('cart_detail')


def add_to_cart_button(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    form = CartAddFlowerForm()
    return render(request, 'shop/flower/add_to_cart.html', {'flower': flower, 'form': form})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    flower=item["flower"],
                    price=item["price"],
                    quantity=item["quantity"]
                )
            cart.clear()

            message = f"📦 Новый заказ #{order.id}\n"
            message += f"👤 {order.first_name} {order.last_name}\n"
            message += f"📞 {order.phone_number}\n"
            message += f"📍 {order.address}\n"
            message += f"🛒 Состав заказа:\n"

            for item in order.items.all():
                message += f" - {item.flower.name} x {item.quantity} ({item.price} ₽)\n"

            message += f"\n💰 Общая сумма: {order.items.aggregate(total=models.Sum(models.F('price') * models.F('quantity')))['total']} ₽"

            send_telegram_message(message)

            return render(request, "shop/order/success.html", {"order": order})

    else:
        form = OrderCreateForm()

    return render(request, "shop/order/create.html", {"cart": cart, "form": form})


def promotion_list(request):
    promotions = PromotionPage.objects.filter(is_active=True)
    return render(request, "shop/promotions/list.html", {"promotions": promotions})

def promotion_detail(request, slug):
    promotion = get_object_or_404(PromotionPage, slug=slug, is_active=True)
    return render(request, "shop/promotions/detail.html", {"promotion": promotion})

