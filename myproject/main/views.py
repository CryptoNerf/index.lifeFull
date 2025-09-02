from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import CustomRegisterForm
from .forms import ProfileForm
from .models import MoodEntry
from .models import Profile
from datetime import datetime, date
import calendar
from django.db.models import Avg


def what_is_index(request):
    return render(request, 'main/what_is_index.html')


@login_required
def account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    avg_rating = None
    if request.user.is_authenticated:
        avg_rating = MoodEntry.objects.filter(user=request.user).aggregate(Avg('rating'))['rating__avg']
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'main/account.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
        'avg_rating': avg_rating
    })

class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['rating', 'note']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }

@login_required
def edit_day(request, day):
    day_date = datetime.strptime(day, "%Y-%m-%d").date()
    try:
        entry = MoodEntry.objects.get(user=request.user, date=day_date)
        created = False
    except MoodEntry.DoesNotExist:
        entry = None
        created = True

    if request.method == 'POST':
        form = MoodEntryForm(request.POST, instance=entry)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.user = request.user
            new_entry.date = day_date
            new_entry.save()
            return redirect('mood_grid')
    else:
        form = MoodEntryForm(instance=entry)

    return render(request, 'main/edit_day.html', {'form': form, 'day': day_date, 'created': created})

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # пароль будет захеширован автоматически
            login(request, user)  # сразу авторизуем
            return redirect('mood_grid')
    else:
        form = CustomRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def mood_grid(request):
    year = date.today().year
    entries = MoodEntry.objects.filter(user=request.user, date__year=year)
    filled_days = set(e.date for e in entries)

    months = []
    for month_num in range(1, 13):
        days_in_month = calendar.monthrange(year, month_num)[1]
        days = []
        for day in range(1, days_in_month + 1):
            d = date(year, month_num, day)
            days.append({
                'date': d,
                'filled': d in filled_days
            })
        months.append({'days': days})

    # Передаем список месяцев для адаптивной сетки
    today = date.today()
    return render(request, 'main/mood_grid.html', {'months': months, 'today': today})
