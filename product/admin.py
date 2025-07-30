from django.contrib import admin
from .models import Category, Image,City,District,Estate,Favorite,Feedback,FeedbackResponse

class EstateAdmin(admin.ModelAdmin):
    list_display=('title','category','city','created_at','is_active')
    list_filter=('category','city','destrict')
    search_fields=('title','description')

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Estate,EstateAdmin)
admin.site.register(Favorite)
admin.site.register(Feedback)
admin.site.register(FeedbackResponse)