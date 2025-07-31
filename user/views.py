from django.shortcuts import render,redirect,get_object_or_404
from .models import MyUser,OTP
from .forms import MyUserRegisterForm,MyUserLoginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .services import generate_otp_code
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


def user_register_view(request):
    if request.method=='POST':
        form=MyUserRegisterForm(request.POST)
        
        
        if form.is_valid():
            form.save()
            messages.success (request,'Вы успешно создали аккаунт')
            return redirect('index')
        
        for field,errors in form.errors.items():
            for error in errors:
                messages.error(request,f'{error}')
        
        
    form =MyUserRegisterForm()
    
    return render(
        request=request,
        template_name='authentication/register.html',
        context={
            "form":form
        }
    )
    
    
def user_login_view(request):
    form = MyUserLoginForm()
    if request.method=='POST':
        form=MyUserLoginForm(request.POST)
        if form.is_valid():
            user_email=form.cleaned_data['email']
            user_password=form.cleaned_data['password']
            
            
            user= authenticate(request,username=user_email,password=user_password)
            
            
        if user:
            if user.is_2fa_enabled:
             otp_code = generate_otp_code()
             OTP.objects.create(
                user=user,
                code=otp_code
            )

            send_mail(
              subject="Одноразовый код для входа в систему ",
              message=f"Ваш одноразовый код: {otp_code}\nНикому не показывайте этот код!",
              from_email=settings.DEFAULT_FROM_EMAIL,
             recipient_list=[user_email],
              fail_silently=False,
            )
            messages.success(request, message='Одноразовый код отправлен на вашу почту')
            return redirect('otp_verify',user.id)
        else:
            login(request,user)
            messages.success(request,'Вы успешно вошли в систему')
            return redirect('index')
        
        messages.error(request, "Пользователь не найден")
        form=MyUserLoginForm()
    return render(
        request=request,
        template_name='authentication/login.html',
        context={
            "form":form
        }
    )
def user_logout_views(request):
    logout(request)
    messages.success(request,'Вы успешно вышли из системы ')
    return redirect('index')


def user_otp_verify_view(request,user_id):
    user=get_object_or_404(MyUser,id=user_id)
    
    
    if request.method=='POST':
        otp_code=request.POST['otp']
        otp=OTP.objects.filter(user=user,code=otp_code).last()
        if otp:
            login(request,user)
            messages.success(request,'вы успешно вошли в систему')
            otp.delete()   
            return redirect('index')
        else:
           messages.error(request,'вы ввели неправильный код ')
    
    return render(
        request=request,
        template_name='authentication/otp_verify.html'
    )
@login_required(login_url='user_login')
def user_profile_view(request):
    current_user=request.user
    if request.method=="POST":
        is_2fa_enabled='is_2fa_enabled' in request.POST
        user=MyUser.objects.get(id=request.user.id)
        user.is_2fa_enabled=is_2fa_enabled
        user.save()
    return render(
        request=request,
        template_name='authentication/user_profile.html',
        context={
            'user':current_user
        }
    )