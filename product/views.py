from django.shortcuts import render
from .models import Category,Estate

def index_view(request):
    parent_categories=Category.objects.filter(parent_category__isnull=True)
    estates=Estate.objects.filter(is_active=True)
    
    
   
    return render(
        request=request,
        template_name='main/index.html',
        context={
            "parent_categories":parent_categories,
            "estates":estates
        }
    )
def estate_detail_view(request):
    return render(
        request=request,
        template_name='main/estate_detail.html'
    )