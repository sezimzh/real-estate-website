from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Estate,Favorite
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Feedback,FeedbackResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Estate
from .filters import EstateFilter

def index_view(request):
    parent_categories = Category.objects.filter(parent_category__isnull=True)
    estates = Estate.objects.filter(is_active=True)[:8]

    if request.user.is_authenticated:
        liked_estates = Favorite.objects.filter(user=request.user).values_list('estate_id', flat=True)
        print(liked_estates)
    else:
        liked_estates = []  

    return render(request, 'main/index.html', {
        'parent_categories': parent_categories,
        'estates': estates,
        'liked_estates': liked_estates
    })
    
   
    #send_mail(
       # subject="Здравствуйте",
       # message="Привет",
       #from_email=settings.DEFAULT_FROM_EMAIL,
      # recipient_list=['ashnld90@gmail.com'],
       #fail_silently=False,
    #)
   
   
   
    return render(
        request=request,
        template_name='main/index.html',
        context={
            "parent_categories":parent_categories,
            "estates":estates,
            "liked_estates": liked_estates 
        }
    )
def estate_detail_view(request,estate_pk):
    estate=get_object_or_404(Estate,id=estate_pk)
    recommended_estates=Estate.objects.filter(category=estate.category).exclude(id=estate.id)
    
    estate_like_count=Favorite.objects.filter(estate=estate).count()
    print(estate)
    
    return render(
        request,
        'main/estate_detail.html',
        {
            'estate': estate,
            'recommended_estates':recommended_estates,
            'estate_like_count':estate_like_count
        }
    )
def user_estate_like_view(request,estate_id):
    estate = get_object_or_404(Estate, id=estate_id)
    like_exist=Favorite.objects.filter(user=request.user,estate=estate).exists()
    if not like_exist:
      like=Favorite(
        user=request.user,
        estate=estate
    )
      like.save()
    else:
        Favorite.objects.filter(user=request.user, estate=estate).delete()

    return redirect('index')

def favorite_estates_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('estate')
    estates = [fav.estate for fav in favorites]
    return render(
        request=request,
        template_name='main/favorites.html',
        context={'estates': estates}
    )
def user_estate_feedback_view(request,estate_pk):
    estate=get_object_or_404(Estate,id=estate_pk)
    
    
    if request.method=='POST':
        comment=request.POST['comment']
        
        Feedback.objects.create(
            user=request.user,
            estate=estate,
            comment=comment
        )
        messages.success(request,'Комментарии добавлено')
        return redirect('detail',estate.id)
    
def user_feedback_response_view(request,feedback_id):
    feedback=get_object_or_404(Feedback,id=feedback_id)
    if request.method =='POST':
        comment=request.POST['comment']
    FeedbackResponse.objects.create(
        user=request.user,
        feedback=feedback,
        comment=comment
    )
    messages.success(request,'Комментарии добавлено')
    return redirect('detail',feedback.estate.id)

def estate_list_view(request):
    estate=EstateFilter(request.GET,queryset=Estate.objects.filter(is_active=True))
    paginator=Paginator(estate.qs,1)
    page_number=request.GET.get("page")
    page_obj = paginator.get_page(page_number)
     
    return render(
        request=request,
        template_name='main/estate_list.html',
        context={
            'estates':estate,
            'page_obj': page_obj,
            
        }
    )