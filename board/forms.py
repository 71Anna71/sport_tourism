from django import forms
from .models import Объявление, Комментарий, ПоходДетали, ГидДетали, СнаряжениеДетали
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class ОбъявлениеForm(forms.ModelForm):
    class Meta:
        model = Объявление
        fields = ['заголовок', 'категория', 'контакты', 'регион', 'изображение', 'описание']

class ПоходДеталиForm(forms.ModelForm):
    class Meta:
        model = ПоходДетали
        fields = ['дата_начала', 'длина_маршрута', 'сложность',  'размер_группы', 'тип_путешествия','требования', 'руководитель', 'стоимость']
        widgets = {
            'дата_начала': forms.DateInput(attrs={'type': 'date'}),
            'стоимость':   forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
        }
class ГидДеталиForm(forms.ModelForm):
    class Meta:
        model = ГидДетали
        fields = ['возраст', 'тип_путешествия', 'опыт']
        widgets = {
                    'возраст': forms.NumberInput(attrs={'min':0}),
                }
        

class СнаряжениеДеталиForm(forms.ModelForm):
    class Meta:
        model = СнаряжениеДетали
        fields = ['вес', 'стоимость']
        widgets = {
            'вес': forms.NumberInput(attrs={'step':'0.01', 'min':0}),
            'стоимость': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
        }

class КомментарийForm(forms.ModelForm):
    class Meta:
        model = Комментарий
        fields = ['текст']
        widgets = {
            'текст': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Оставьте комментарий...'}),
        }



        
class РегистрацияForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Роль")
    email = forms.EmailField(required=True, label="Email")  # Добавили email

#    username = forms.CharField(
#        label=_("Имя пользователя"),
#        max_length=150,
#        widget=forms.TextInput(attrs={'placeholder': _('Имя пользователя')})
#    )
#    password1 = forms.CharField(
#        label=_("Пароль"),
#        widget=forms.PasswordInput(attrs={'placeholder': _('Пароль')}),
#        help_text=_("Пароль должен содержать минимум 8 символов.")
#    )
#    password2 = forms.CharField(
#        label=_("Подтверждение пароля"),
#        widget=forms.PasswordInput(attrs={'placeholder': _('Подтверждение пароля')}),
#        help_text=_("Введите тот же пароль ещё раз для проверки.")
#    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]  # Сохраняем email
        # Остальные поля, если нужно, можно обработать тут
        if commit:
            user.save()
        return user