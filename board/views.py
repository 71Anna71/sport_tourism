from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Объявление, Категория,  ПоходДетали, ГидДетали, СнаряжениеДетали,  Комментарий
from .forms import ОбъявлениеForm, ПоходДеталиForm, ГидДеталиForm , СнаряжениеДеталиForm, КомментарийForm, РегистрацияForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import РегистрацияForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .forms import РегистрацияForm
from django.db import models
from django.views.decorators.http import require_POST


User = get_user_model()
#def index(request):
 #   category_id = request.GET.get('category')
 #   if category_id:
 ##       объявления = Объявление.objects.filter(категория_id=category_id)
 #   else:
 ##       объявления = Объявление.objects.all()
 #   категории = Категория.objects.all()
 #   return render(request, 'board/index.html', {'объявления': объявления, 'категории': категории})
def index(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')

    
    region = request.GET.get('region', '')
    difficulty = request.GET.get('difficulty', '')
    trip_type = request.GET.get('trip_type', '')
    guide_trip_type = request.GET.get('guide_trip_type', '')
    cost = request.GET.get('cost', '')
    объявления = Объявление.objects.filter(is_active=True)
   # объявления = Объявление.objects.all()
   

    if category_id:
        объявления = объявления.filter(категория_id=category_id)

    # Поиск по названию/описанию
    if q:
        объявления = объявления.filter(
            models.Q(заголовок__icontains=q) | models.Q(описание__icontains=q)
        )

    # Фильтры только если категория "Поход"
    if category_id:
        try:
            category_obj = Категория.objects.get(pk=category_id)
            if category_obj.название == "Поход":
                if region:
                    объявления = объявления.filter(регион=region)
                if difficulty:
                    объявления = объявления.filter(поход_детали__сложность=difficulty)
                if trip_type:
                    объявления = объявления.filter(поход_детали__тип_путешествия=trip_type)
                if cost:
                    cost_min, cost_max = cost.split('-')
                    объявления = объявления.filter(поход_детали__стоимость__gte=cost_min, поход_детали__стоимость__lte=cost_max)
            elif category_obj.название == "Гид":
                if guide_trip_type:
                    объявления = объявления.filter(гид_детали__тип_путешествия=guide_trip_type)
        
        except Категория.DoesNotExist:
            pass

    категории = Категория.objects.all()
    regions = Объявление.objects.values_list('регион', flat=True).distinct()
    hike_category = Категория.objects.get(название="Поход")  # или по слагу, если есть
    hike_category_id = str(hike_category.id)  # строкой для сравнения в шаблоне

    difficulties = [d[0] for d in ПоходДетали._meta.get_field('сложность').choices]
    return render(request, 'board/index.html', {
        'объявления': объявления,
        'категории': категории,
        'regions': regions,
        'hike_category_id': hike_category_id,
        'difficulties': difficulties,
    })
 #   if q:
 #       объявления = объявления.filter(заголовок__icontains=q)  # поиск по названию

    # Фильтры только если категория "Поход"
#    if category_id:
#        try:
###            category_obj = Категория.objects.get(pk=category_id)
  #         if category_obj.название == "Поход":
   #             if region:
    #                объявления = объявления.filter(регион=region)
     #           if difficulty:
      #              объявления = объявления.filter(поход_детали__сложность=difficulty)
       #         if trip_type:
        #            объявления = объявления.filter(поход_детали__тип_путешествия=trip_type)
         #       if cost:
          #          cost_min, cost_max = cost.split('-')
           #         объявления = объявления.filter(поход_детали__стоимость__gte=cost_min, поход_детали__стоимость__lte=cost_max)
 #       except Категория.DoesNotExist:
  #          pass

 #   категории = Категория.objects.all()
 #   regions = Объявление.objects.values_list('регион', flat=True).distinct()
 ##   difficulties = [d[0] for d in ПоходДетали._meta.get_field('сложность').choices]
   # return render(request, 'board/index.html', {
    #    'объявления': объявления,
     #   'категории': категории,
      #  'regions': regions,
       # 'difficulties': difficulties,
  #  })


@login_required
def all_users(request):
    if not request.user.is_superuser:
        return redirect('index')
    users = User.objects.all()
    return render(request, 'board/all_users.html', {'users': users})




def ad_detail(request, pk):
    ad = get_object_or_404(Объявление, pk=pk)
    ad.просмотры += 1
    ad.save(update_fields=["просмотры"])

    комментарии = ad.комментарии.all().order_by('-дата_создания')
    form = КомментарийForm()
    походы_гида = None
    # Если это гид — выводим связанные походы
    if ad.категория.название == "Гид":
        # Все объявления типа "Поход", где автор — этот же пользователь
        походы_гида = Объявление.objects.filter(author=ad.author, категория__название="Поход")
    return render(
        request, 'board/ad_detail.html',
        {
            'ad': ad,
            'комментарии': комментарии,
            'form': form,
            'походы_гида': походы_гида,
        }
    )



@login_required
def add_ad(request):
    if request.method == "POST":
        form = ОбъявлениеForm(request.POST, request.FILES)
        pohod_form = ПоходДеталиForm(request.POST)
        gid_form = ГидДеталиForm(request.POST)
        snar_form    = СнаряжениеДеталиForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            # Сохраняем детали похода, если категория "Поход"
            # Поход
            if ad.категория and ad.категория.название == "Поход" and pohod_form.is_valid():
                det = pohod_form.save(commit=False)
                det.объявление = ad
                det.save()
            # Гид
            if ad.категория and ad.категория.название == "Гид" and gid_form.is_valid():
                det = gid_form.save(commit=False)
                det.объявление = ad
                det.save()
            
            if ad.категория and ad.категория.название == "Снаряжение" and snar_form.is_valid():
                det = snar_form.save(commit=False)
                det.объявление = ad
                det.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = ОбъявлениеForm()
        pohod_form = ПоходДеталиForm()
        gid_form = ГидДеталиForm()
        snar_form  = СнаряжениеДеталиForm()

    return render(request, "board/add_ad.html", {
        "form": form,
        "pohod_form": pohod_form,
        "gid_form": gid_form,
        "snar_form": snar_form,
    })


from django.contrib.auth.decorators import login_required

@login_required
def my_ads(request):
    объявления = Объявление.objects.filter(author=request.user)
    return render(request, 'board/my_ads.html', {
        'объявления': объявления,
        'my_ads': True  # для шаблона (выделение кнопки, если надо)
    })

@login_required
@require_POST
def mark_inactive(request, pk):
    ad = get_object_or_404(Объявление, pk=pk)
    if ad.author != request.user:
        return HttpResponseForbidden("Вы не автор объявления.")
    ad.is_active = False
    ad.save()
    return redirect('ad_detail', pk=ad.pk)

@login_required
def add_comment(request, pk):
    объявление = get_object_or_404(Объявление, pk=pk)
    if request.method == 'POST':
        form = КомментарийForm(request.POST)
        if form.is_valid():
            комментарий = form.save(commit=False)
            комментарий.пользователь = request.user
            комментарий.объявление = объявление
            комментарий.save()
            return redirect('ad_detail', pk=pk)
    return redirect('ad_detail', pk=pk)

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Объявление, pk=pk)
    if ad.author != request.user:
        return HttpResponseForbidden('Вы не являетесь автором этого объявления.')
    if request.method == 'POST':
        form = ОбъявлениеForm(request.POST, request.FILES, instance=ad)
        # Поход
        if ad.категория.название == "Поход":
            pohod_form = ПоходДеталиForm(request.POST, instance=getattr(ad, 'поход_детали', None))
        else:
            pohod_form = None
        # Гид
        if ad.категория.название == "Гид":
            gid_form = ГидДеталиForm(request.POST, instance=getattr(ad, 'гид_детали', None))
        else:
            gid_form = None
        # Снаряжение
        if ad.категория.название == "Снаряжение":
            snar_form = СнаряжениеДеталиForm(request.POST, instance=getattr(ad, 'снаряжение_детали', None))
        else:
            snar_form = None

        # Сохраняем всё
        if form.is_valid():
            ad = form.save()
            if pohod_form and pohod_form.is_valid():
                pohod_det = pohod_form.save(commit=False)
                pohod_det.объявление = ad
                pohod_det.save()
            if gid_form and gid_form.is_valid():
                gid_det = gid_form.save(commit=False)
                gid_det.объявление = ad
                gid_det.save()
            if snar_form and snar_form.is_valid():
                snar_det = snar_form.save(commit=False)
                snar_det.объявление = ad
                snar_det.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = ОбъявлениеForm(instance=ad)
        pohod_form = gid_form = snar_form = None
        if ad.категория.название == "Поход":
            pohod_form = ПоходДеталиForm(instance=getattr(ad, 'поход_детали', None))
        if ad.категория.название == "Гид":
            gid_form = ГидДеталиForm(instance=getattr(ad, 'гид_детали', None))
        if ad.категория.название == "Снаряжение":
            snar_form = СнаряжениеДеталиForm(instance=getattr(ad, 'снаряжение_детали', None))
        
    return render(request, 'board/edit_ad.html', {
        'form': form,
        'ad': ad,
        'pohod_form': pohod_form,
        'gid_form': gid_form,
        'snar_form': snar_form,
    })


def is_admin(user):
    return user.is_superuser




# Проверка, что пользователь — админ
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@user_passes_test(is_admin)
def all_users(request):
    users = User.objects.all()
    return render(request, 'board/all_users.html', {'users': users})

@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('all_users')
    return render(request, 'board/edit_user.html', {'user': user})

@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('all_users')
    return render(request, 'board/delete_user.html', {'user': user})




def user_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
   # объявления = Объявление.objects.filter(author=user_obj)
    объявления = Объявление.objects.filter(author=user_obj)  # Показывает все, и актуальные, и нет


    #return render(request, 'board/user_profile.html', {'profile_user': user_obj, 'объявления': объявления})
    count_ads = объявления.count()
    count_views = объявления.aggregate(models.Sum("просмотры"))["просмотры__sum"] or 0
    count_comments = sum(ad.комментарии.count() for ad in объявления)
    return render(request, 'board/user_profile.html', {
        'profile_user': user_obj,
        'объявления': объявления,
        'count_ads': count_ads,
        'count_views': count_views,
        'count_comments': count_comments,
    })

@login_required
def toggle_favorite(request, pk):
    ad = get_object_or_404(Объявление, pk=pk)
    if request.user in ad.избранное.all():
        ad.избранное.remove(request.user)
    else:
        ad.избранное.add(request.user)
    return redirect('ad_detail', pk=pk)



@login_required
def favorites_list(request):
    fav_ads = request.user.favorite_ads.all()
    return render(request, 'board/favorites.html', {'объявления': fav_ads})





def signup(request):
    if request.method == 'POST':
        form = РегистрацияForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            # По умолчанию обычный пользователь
            user.is_staff = False
            user.is_superuser = False
            if role == 'admin':
                user.is_staff = True  # Даст доступ к /admin, если нужно
                # Если хочешь сделать полным суперюзером:
                # user.is_superuser = True
            user.save()
            messages.success(request, 'Регистрация прошла успешно! Вы вошли как {}.'.format(user.username))
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте правильность заполнения формы.')
    else:
        form = РегистрацияForm()
    return render(request, 'board/signup.html', {'form': form})











#def signup(request):
#    if request.method == 'POST':
##        form = РегистрацияForm(request.POST)
 #       if form.is_valid():
 #           user = form.save()
 #           login(request, user)
 #           return redirect('index')
 #   else:
 #       form = РегистрацияForm()
 #   return render(request, 'board/signup.html', {'form': form})















#@login_required
#def edit_ad(request, pk):
#    ad = get_object_or_404(Объявление, pk=pk)
#    # Только автор может редактировать
#    if ad.author != request.user:
#        return HttpResponseForbidden('Вы не являетесь автором этого объявления.')
#    if request.method == 'POST':
#        form = ОбъявлениеForm(request.POST, instance=ad)
#        if form.is_valid():
#            form.save()
#            return redirect('index')
#    else:
#        form = ОбъявлениеForm(instance=ad)
#    return render(request, 'board/edit_ad.html', {'form': form})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Объявление, pk=pk)
    # Только автор может удалять
    if ad.author != request.user:
        return HttpResponseForbidden('Вы не являетесь автором этого объявления.')
    if request.method == 'POST':
        ad.delete()
        return redirect('index')
    return render(request, 'board/delete_ad.html', {'ad': ad})


def delete_comment(request, comment_id):
    комментарий = get_object_or_404(Комментарий, pk=comment_id)
    объявление = комментарий.объявление

    # Только суперпользователь может удалять любой комментарий,
    # или автор комментария (если хочешь оставить такую опцию)
    if request.user.is_superuser or комментарий.пользователь == request.user:
        комментарий.delete()
        return redirect('ad_detail', pk=объявление.pk)
    return redirect('ad_detail', pk=объявление.pk)

