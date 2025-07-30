from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Estate,Favorite
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
from django.core.mail import send_mail
from django.conf import settings

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
    comments = Comment.objects.filter(estate=estate).order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.estate = estate
            comment.user = request.user
            comment.save()
            return redirect('detail', estate_pk=estate_pk)

    return render(
        request,
        'main/estate_detail.html',
        {
            'estate': estate,
            'comments': comments,
            'form': form,
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