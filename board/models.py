from django.db import models
from django.contrib.auth.models import User


class Категория(models.Model):
    название = models.CharField(max_length=255)

    def __str__(self):
        return self.название

    
class Объявление(models.Model):
    заголовок = models.CharField(max_length=255)
    категория = models.ForeignKey(Категория, on_delete=models.CASCADE, null=True, blank=True)
    контакты       = models.CharField(max_length=255, blank=True, null=True)
    регион         = models.CharField(max_length=255, blank=True, null=True)
    описание = models.TextField(blank=True, null=True, default="")
    дата_создания = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    изображение = models.ImageField(upload_to='ads_images/', blank=True, null=True)  # Новое поле
    избранное = models.ManyToManyField(User, related_name="favorite_ads", blank=True,db_table="board_объявление_избранное_v2")
    просмотры = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField("Актуально", default=True)
    def __str__(self):
            return self.заголовок

    
class ПоходДетали(models.Model):
    объявление = models.OneToOneField(Объявление, on_delete=models.CASCADE, related_name="поход_детали")
    дата_начала = models.CharField(max_length=100, blank=True, null=True)
    длина_маршрута = models.CharField(max_length=100, blank=True, null=True)
    сложность       = models.CharField(
                         max_length=50,
                         choices=[
                             ('1 к.с.', '1 к.с.'),
                             ('2 к.с.', '2 к.с.'),
                             ('3 к.с.', '3 к.с.'),
                             ('4 к.с.', '4 к.с.'),
                             ('5 к.с.', '5 к.с.'),
                             ('6 к.с.', '6 к.с.'),
                             ('ПВД', 'ПВД'),
                         ]
                       )
    тип_путешествия = models.CharField(
                         max_length=50,
                         choices=[
                             ('Пеший', 'Пеший'),
                             ('Лыжный', 'Лыжный'),
                             ('Водный', 'Водный'),
                             ('Горный', 'Горный'),
                         ]
                       )
    размер_группы = models.CharField(max_length=50, blank=True, null=True)
    требования = models.TextField(blank=True, null=True)
    руководитель    = models.CharField(max_length=100)
    стоимость = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    #длительность = models.CharField(max_length=50, blank=True, null=True)
   # тип_путешествия = models.CharField(max_length=50, blank=True, null=True)
    #требования = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Детали похода: {self.объявление.заголовок}"

class ГидДетали(models.Model):
    объявление = models.OneToOneField(Объявление, on_delete=models.CASCADE, related_name='гид_детали')
    возраст = models.PositiveIntegerField(null=True, blank=True)
    тип_путешествия = models.CharField(
                         max_length=50,
                         choices=[
                             ('Пеший', 'Пеший'),
                             ('Лыжный', 'Лыжный'),
                             ('Водный', 'Водный'),
                             ('Горный', 'Горный'),
                         ]
                       )
    опыт = models.CharField(
        max_length=100,
        blank=True, null=True,
        help_text="Опыт руководства (например, «5 лет»)"
    )

    def __str__(self):
        return f'Гид: {self.объявление.заголовок}'
    
class СнаряжениеДетали(models.Model):
    объявление  = models.OneToOneField(Объявление, on_delete=models.CASCADE, related_name='снаряжение_детали')
    вес = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    стоимость = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f'Снаряжение: {self.объявление.заголовок}'

# Create your models here.

class Комментарий(models.Model):
    объявление      = models.ForeignKey(Объявление, on_delete=models.CASCADE, related_name='комментарии')
    пользователь    = models.ForeignKey(User, on_delete=models.CASCADE)
    текст           = models.TextField("Комментарий")
    дата_создания   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.пользователь.username}: {self.текст[:30]}"