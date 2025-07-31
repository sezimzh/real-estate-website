from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from product.constans import NULLABLE
from user.choices import MyUserRoleEnum


class MyUserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        
        user = self.model(
        username=username,
        email=self.normalize_email(email)
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None):
        user=self.create_user(
            username=username,
            email=email
        )
        user.is_admin=True
        user.set_password(password)
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    username=models.CharField(max_length=222,verbose_name='имя пользователя')
    email=models.EmailField(unique=True,verbose_name='адрес электронной почты')
    avatar=models.ImageField(upload_to='media/user_avatars',**NULLABLE,verbose_name='аватар')
    role=models.CharField(
        max_length=20,
        choices=MyUserRoleEnum.choices,
        default=MyUserRoleEnum.STANDARD_USER,
        verbose_name='Роль'
    )
    balance=models.DecimalField(default=0,decimal_places=2,max_digits=12,verbose_name='Баланс')
    is_admin = models.BooleanField(
        default=False
    )
    is_2fa_enabled=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now=True)
    
    objects=MyUserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

class OTP(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)