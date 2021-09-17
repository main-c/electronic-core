from core.models import Category, Product
import random

def categories(request):
    categories = Category.objects.all()

    return {'categories': categories}

