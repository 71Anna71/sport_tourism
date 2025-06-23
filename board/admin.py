from django.contrib import admin
from .models import Объявление, Категория, Комментарий

admin.site.register(Объявление)
admin.site.register(Категория) 
admin.site.register(Комментарий)
# Register your models here.
