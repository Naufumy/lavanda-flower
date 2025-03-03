from shop.models import PromotionPage

def promotions_context(request):
    return {"promotions": PromotionPage.objects.filter(is_active=True)}