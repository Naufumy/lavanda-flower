from django.urls import path
from .views import flower_list, flower_detail, cart_detail, cart_add, cart_remove, order_create, promotion_list, promotion_detail

urlpatterns = [
    path('', flower_list, name='flower_list'),
    path('flower/<int:flower_id>/', flower_detail, name='flower_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:flower_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:flower_id>/', cart_remove, name='cart_remove'),
    path("order/create/", order_create, name="order_create"),
    path("promotions/", promotion_list, name="promotion_list"),
    path("promotions/<slug:slug>/", promotion_detail, name="promotion_detail"),
]
