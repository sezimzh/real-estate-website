from django.db import models
from product.constans import NULLABLE 

class Category(models.Model):
    title=models.CharField(max_length=223,verbose_name='Название')
    parent_category=models.ForeignKey('self',on_delete=models.CASCADE,**NULLABLE,verbose_name='Родительская категория')
    
    
class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'

def __str__(self):
    ancestors = []
    category = self
    while category:
        ancestors.append(category.title)
        category = category.parent_category
    return ' > '.join(reversed(ancestors))


class City(models.Model):
    title=models.CharField(max_length=223,verbose_name='Название')
    

    def __str__(self):
        return self.title
    
    
class District(models.Model):
    city=models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Город')
    title=models.CharField(max_length=223,verbose_name='Название')
    
    
    def __str__(self):
        return self.title
    
class Image(models.Model):
    product=models.ForeignKey('Estate',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/additional_image')
    
    
class Estate(models.Model):
    title=models.CharField(max_length=223,verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,verbose_name='Категория')
    cover=models.ImageField(upload_to='media/products_image',verbose_name='Обложка')
    area=models.DecimalField(decimal_places=1,max_digits=12,verbose_name='Кол-во кв метров')
    city=models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Город')
    destrict= models.ForeignKey(District,on_delete=models.PROTECT,verbose_name='Район')
    geo=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=12,verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    promo_video=models.FileField(upload_to='media/product_promo_video',verbose_name='Промо ролик ')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    update_at=models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    
    
class Meta:
    verbos_name='Недвижимость'
    verbos_name='Недвижимости'
