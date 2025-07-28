from django.shortcuts import render,redirect
from .models import MyUser
from .forms import MyUserRegisterForm,MyUserLoginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout

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
                login(request,user)
                messages.success(request,'Все классно')
                return redirect('index')
        
        messages.error(request,'Неправильный логин или пароль')
        
        
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