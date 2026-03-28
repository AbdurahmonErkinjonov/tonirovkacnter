from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
from datetime import datetime, date, timedelta
import math
from .models import *
from .forms import *
from .decorators import admin_required, worker_required
from datetime import datetime, timedelta, date
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Worker


# -------------------- Authentication --------------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('worker_dashboard')
        messages.error(request, "Login yoki parol noto'g'ri!")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_redirect(request):
    return redirect('login')

# -------------------- Admin views --------------------

@admin_required
def admin_dashboard(request):
    workers = Worker.objects.all()
    today = date.today()
    
    today_works = WorkDone.objects.filter(date=today, is_confirmed=True)
    today_works_count = today_works.count()
    today_income = today_works.aggregate(Sum('total_price'))['total_price__sum'] or 0
    today_sessions = WorkSession.objects.filter(check_in__date=today)
    present_workers = today_sessions.filter(check_out__isnull=True).count()
    
    context = {
        'workers': workers,
        'total_workers': workers.count(),
        'today_works': today_works_count,
        'today_income': today_income,
        'present_workers': present_workers,
        'recent_works': WorkDone.objects.filter(is_confirmed=True).order_by('-confirmed_at')[:10],
    }
    return render(request, 'admin_panel/dashboard.html', context)

@admin_required
def workers_list(request):
    workers = Worker.objects.all()
    return render(request, 'admin_panel/workers_list.html', {'workers': workers})

@admin_required
def edit_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == 'POST':
        form = WorkerEditForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, f"{worker.full_name} ma'lumotlari yangilandi!")
            return redirect('workers_list')
    else:
        form = WorkerEditForm(instance=worker)
    return render(request, 'admin_panel/edit_worker.html', {'form': form, 'worker': worker})

@admin_required
def add_worker(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu login band!")
            else:
                user = User.objects.create_user(username=username, password=password)
                worker = form.save(commit=False)
                worker.user = user
                worker.save()
                messages.success(request, f"Ishchi {worker.full_name} muvaffaqiyatli qo'shildi!")
                return redirect('admin_dashboard')
    else:
        form = WorkerForm()
    
    return render(request, 'admin_panel/add_worker.html', {'form': form})

@admin_required
def add_holiday(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dam olish kuni qo'shildi!")
            return redirect('admin_dashboard')
    else:
        form = HolidayForm()
    
    return render(request, 'admin_panel/add_holiday.html', {'form': form})

@admin_required
def add_tonirovka(request):
    if request.method == 'POST':
        form = TonirovkaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tonirovka qo'shildi!")
            return redirect('admin_dashboard')
    else:
        form = TonirovkaForm()
    
    return render(request, 'admin_panel/add_tonirovka.html', {'form': form})

@admin_required
def add_sonsa(request):
    if request.method == 'POST':
        form = SonsaZashitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sonsa zashita qo'shildi!")
            return redirect('admin_dashboard')
    else:
        form = SonsaZashitaForm()
    
    return render(request, 'admin_panel/add_sonsa.html', {'form': form})

@admin_required
def add_laminatsiya(request):
    if request.method == 'POST':
        form = LaminationFilmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Laminatsiya plyonkasi qo'shildi!")
            return redirect('admin_dashboard')
    else:
        form = LaminationFilmForm()
    
    return render(request, 'admin_panel/add_laminatsiya.html', {'form': form})

@admin_required
def add_bron(request):
    if request.method == 'POST':
        form = ProtectiveFilmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bron plyonka qo'shildi!")
            return redirect('admin_dashboard')
    else:
        form = ProtectiveFilmForm()
    
    return render(request, 'admin_panel/add_bron.html', {'form': form})

@admin_required
def add_bonus(request):
    if request.method == 'POST':
        form = BonusForm(request.POST)
        if form.is_valid():
            bonus = form.save()
            messages.success(request, f"✅ {bonus.worker.full_name} ga {bonus.amount} so'm bonus berildi!")
            return redirect('admin_dashboard')
    else:
        form = BonusForm()
    
    return render(request, 'admin_panel/add_bonus.html', {'form': form})

@admin_required
def salary_paid(request):
    if request.method == 'POST':
        form = SalaryPaidForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            worker.reset_monthly()
            messages.success(request, f"{worker.full_name} ning oyligi to'landi! Barcha hisoblar 0 ga tenglashtirildi.")
            return redirect('admin_dashboard')
    else:
        form = SalaryPaidForm()
    
    return render(request, 'admin_panel/salary_paid.html', {'form': form})

@admin_required
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"{payment.worker.full_name} dan {payment.amount} so'm pul olindi!")
            return redirect('admin_dashboard')
    else:
        form = PaymentForm()
    
    return render(request, 'admin_panel/payment.html', {'form': form})

@admin_required
def reports(request):
    workers = Worker.objects.all()
    
    year = request.GET.get('year', date.today().year)
    month = request.GET.get('month', date.today().month)
    worker_id = request.GET.get('worker')
    
    try:
        year = int(year)
        month = int(month)
    except:
        year = date.today().year
        month = date.today().month
    
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)
    
    works = WorkDone.objects.filter(
        date__gte=month_start,
        date__lte=month_end,
        is_confirmed=True
    )
    
    if worker_id:
        works = works.filter(worker_id=worker_id)
    
    years = range(2024, date.today().year + 2)
    months = [
        (1, 'Yanvar'), (2, 'Fevral'), (3, 'Mart'), (4, 'Aprel'),
        (5, 'May'), (6, 'Iyun'), (7, 'Iyul'), (8, 'Avgust'),
        (9, 'Sentabr'), (10, 'Oktabr'), (11, 'Noyabr'), (12, 'Dekabr')
    ]
    
    context = {
        'workers': workers,
        'works': works.order_by('-date'),
        'year': year,
        'month': month,
        'years': years,
        'months': months,
        'month_name': dict(months)[month],
        'total_income': works.aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'total_share': works.aggregate(Sum('worker_share'))['worker_share__sum'] or 0,
    }
    return render(request, 'admin_panel/reports.html', context)

# -------------------- Worker views --------------------

@worker_required
def worker_dashboard(request):
    worker = request.user.worker
    today = date.today()
    month_start = date(today.year, today.month, 1)
    
    month_works = WorkDone.objects.filter(
        worker=worker,
        date__gte=month_start,
        is_confirmed=True
    )
    
    month_sessions = WorkSession.objects.filter(
        worker=worker,
        check_in__date__gte=month_start
    )
    
    month_fines = month_sessions.aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    month_bonuses = month_sessions.aggregate(Sum('bonus_amount'))['bonus_amount__sum'] or 0
    
    net_salary = worker.net_salary()
    
    # Bugun ish kuni ekanligini tekshirish
    is_working_day = worker.is_working_day(today)
    
    # Kelajakdagi dam olish kunlari (bugundan keyingi 30 kun)
    future_holidays = Holiday.objects.filter(date__gte=today).order_by('date')[:10]
    
    # Bugungi seans
    today_session = WorkSession.objects.filter(worker=worker, check_in__date=today).first()
    
    # 3 soatlik bonus tekshirish
    three_hour_bonus_added = False
    three_hour_bonus_amount = 0
    three_hour_bonus_blocks = 0
    three_hour_added_blocks = 0
    
    if today_session and not today_session.check_out and worker.three_hour_bonus_amount > 0:
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        check_in = today_session.check_in
        interval_hours = 3
        interval_seconds = interval_hours * 3600
        
        # Necha interval o'tgan
        seconds_passed = (now - check_in).total_seconds()
        current_blocks = today_session.three_hour_bonus_blocks or 0
        new_blocks = int(seconds_passed // interval_seconds)
        
        if new_blocks > current_blocks:
            add_blocks = new_blocks - current_blocks
            bonus_amount = worker.three_hour_bonus_amount * add_blocks
            
            today_session.three_hour_bonus_blocks = new_blocks
            today_session.three_hour_total_bonus = (today_session.three_hour_total_bonus or 0) + bonus_amount
            today_session.last_bonus_check = now
            today_session.save()
            
            worker.total_bonuses += bonus_amount
            worker.save()
            
            three_hour_bonus_added = True
            three_hour_bonus_amount = bonus_amount
            three_hour_bonus_blocks = new_blocks
            three_hour_added_blocks = add_blocks
    
    context = {
        'worker': worker,
        'today': today,
        'is_holiday': Holiday.objects.filter(date=today).exists(),
        'is_working_day': is_working_day,
        'today_session': today_session,
        'month_fines': month_fines,
        'month_bonuses': month_bonuses,
        'net_salary': net_salary,
        'remaining_debt': worker.remaining_debt(),
        'recent_works': WorkDone.objects.filter(
            worker=worker, 
            is_confirmed=True
        ).order_by('-confirmed_at')[:10],
        'future_holidays': future_holidays,
        'three_hour_bonus_added': three_hour_bonus_added,
        'three_hour_bonus_amount': three_hour_bonus_amount,
        'three_hour_bonus_blocks': three_hour_bonus_blocks,
        'three_hour_added_blocks': three_hour_added_blocks,
    }
    return render(request, 'worker_panel/dashboard.html', context)

@worker_required
def check_in(request):
    if request.method == 'POST':
        worker = request.user.worker
        today = date.today()
        
        if Holiday.objects.filter(date=today).exists():
            messages.error(request, "Bugun dam olish kuni!")
            return redirect('worker_dashboard')
        
        if WorkSession.objects.filter(worker=worker, check_in__date=today).exists():
            messages.error(request, "Siz allaqachon kelgan deb belgilagansiz!")
            return redirect('worker_dashboard')
        
        lat = float(request.POST.get('lat', 0))
        lng = float(request.POST.get('lng', 0))
        
        # Joylashuvni tekshirish
        distance = math.sqrt((lat - settings.CENTER_LAT)**2 + (lng - settings.CENTER_LNG)**2) * 111000
        if distance > settings.ALLOWED_RADIUS:
            messages.error(request, f"Siz ish joyidan {distance:.0f} metr uzoqdasiz!")
            return redirect('worker_dashboard')
        
        # Kechikishni hisoblash
        now = timezone.now()
        current_time = now.time()
        weekday = today.weekday()
        start_time = getattr(worker, ['monday_start', 'tuesday_start', 'wednesday_start', 
                                      'thursday_start', 'friday_start', 'saturday_start', 'sunday_start'][weekday])
        
        late_minutes = 0
        fine = 0
        
        # Ish kuni ekanligini tekshirish
        is_working_day = worker.is_working_day(today)
        
        if is_working_day and current_time > start_time:
            late_minutes = (datetime.combine(today, current_time) - datetime.combine(today, start_time)).seconds // 60
            if late_minutes >= 10:
                full_blocks = late_minutes // 10
                fine = worker.late_fine * full_blocks
        
        # Session yaratish (3 soatlik bonus uchun maydonlar qo'shildi)
        session = WorkSession.objects.create(
            worker=worker,
            check_in=now,
            check_in_lat=lat,
            check_in_lng=lng,
            is_late=(late_minutes >= 10 and is_working_day),
            fine_amount=fine,
            is_off_day=not is_working_day,
            three_hour_bonus_blocks=0,      # Yangi qo'shildi
            three_hour_total_bonus=0,       # Yangi qo'shildi
            last_bonus_check=now            # Yangi qo'shildi
        )
        
        if fine > 0:
            worker.total_fines += fine
            worker.save()
            messages.warning(
                request, 
                f"{late_minutes} daqiqa kechikdingiz! "
                f"Jarima: {fine} so'm (faqat to'liq 10 daqiqalik bloklar uchun)."
            )
        else:
            if late_minutes > 0 and is_working_day:
                messages.info(
                    request, 
                    f"{late_minutes} daqiqa kechikdingiz, "
                    f"lekin 10 daqiqa to'lmagani uchun jarima yo'q."
                )
            elif not is_working_day:
                messages.info(request, "Bugun dam olish kuningiz. Kelganingiz uchun admin bonus qo'shishi mumkin.")
            else:
                messages.success(request, "Keldingiz belgilandi!")
    
    return redirect('worker_dashboard')



@worker_required
def check_out(request):
    if request.method == 'POST':
        worker = request.user.worker
        today = date.today()
        
        session = WorkSession.objects.filter(worker=worker, check_in__date=today).first()
        if not session or session.check_out:
            messages.error(request, "Xatolik yuz berdi!")
            return redirect('worker_dashboard')
        
        lat = float(request.POST.get('lat', 0))
        lng = float(request.POST.get('lng', 0))
        
        distance = math.sqrt((lat - settings.CENTER_LAT)**2 + (lng - settings.CENTER_LNG)**2) * 111000
        if distance > settings.ALLOWED_RADIUS:
            messages.error(request, f"Siz ish joyidan {distance:.0f} metr uzoqdasiz!")
            return redirect('worker_dashboard')
        
        now = timezone.now()
        session.check_out = now
        session.check_out_lat = lat
        session.check_out_lng = lng
        
        # Qo'shimcha ish vaqtini hisoblash (faqat ish kunlari uchun)
        weekday = today.weekday()
        end_time = getattr(worker, ['monday_end', 'tuesday_end', 'wednesday_end', 
                                    'thursday_end', 'friday_end', 'saturday_end', 'sunday_end'][weekday])
        
        work_end = timezone.make_aware(datetime.combine(today, end_time))
        bonus = 0
        overtime_minutes = 0
        
        if now > work_end and worker.is_working_day(today):
            overtime_minutes = (now - work_end).seconds // 60
            # FAQAT 1 MARTA, 1 SOATDAN OSHGANDA BONUS QO'SHILADI
            if overtime_minutes >= 60:
                bonus = worker.overtime_bonus
            
            session.overtime_minutes = overtime_minutes
            session.bonus_amount = bonus
            
            if bonus > 0:
                worker.total_bonuses += bonus
                worker.save()
        
        session.save()
        
        if bonus > 0:
            hours = overtime_minutes // 60
            minutes = overtime_minutes % 60
            msg = f"Ketishingiz belgilandi! Qo'shimcha ish: {hours} soat {minutes} daqiqa. "
            msg += f"Bonus: {bonus} so'm"
            messages.success(request, msg)
        else:
            if overtime_minutes > 0:
                messages.info(
                    request, 
                    f"Ketishingiz belgilandi! {overtime_minutes} daqiqa qo'shimcha ishlagansiz, "
                    f"lekin 1 soat to'lmagani uchun bonus yo'q."
                )
            else:
                messages.success(request, "Ketishingiz belgilandi!")
    
    return redirect('worker_dashboard')



@worker_required
def tonirovka_work(request):
    if request.method == 'POST':
        form = TonirovkaWorkForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            tonirovka = form.cleaned_data['tonirovka']
            car_name = form.cleaned_data['car_name']
            
            # Uvol qiymatlari
            rear_door = form.cleaned_data['rear_door']
            front_door = form.cleaned_data['front_door']
            rear_windshield = form.cleaned_data['rear_windshield']
            front_windshield = form.cleaned_data['front_windshield']
            
            # Checkbox qiymatlari (qaysi qismlar ishlangan)
            rear_door_done = request.POST.get('rear_door_done') == 'on'
            front_door_done = request.POST.get('front_door_done') == 'on'
            rear_windshield_done = request.POST.get('rear_windshield_done') == 'on'
            front_windshield_done = request.POST.get('front_windshield_done') == 'on'
            
            # Tanlangan qismlarni JSON formatda saqlash
            selected_parts = []
            
            # Uvol va ishlangan qism ma'lumotlarini birlashtirish
            if rear_door_done or rear_door > 0:
                selected_parts.append({
                    'key': 'rear_door', 
                    'name': 'Orqa eshik', 
                    'count': rear_door, 
                    'done': rear_door_done
                })
                
            if front_door_done or front_door > 0:
                selected_parts.append({
                    'key': 'front_door', 
                    'name': 'Oldi eshik', 
                    'count': front_door, 
                    'done': front_door_done
                })
                
            if rear_windshield_done or rear_windshield > 0:
                selected_parts.append({
                    'key': 'rear_windshield', 
                    'name': 'Orqa lobovoy', 
                    'count': rear_windshield, 
                    'done': rear_windshield_done
                })
                
            if front_windshield_done or front_windshield > 0:
                selected_parts.append({
                    'key': 'front_windshield', 
                    'name': 'Oldi lobovoy', 
                    'count': front_windshield, 
                    'done': front_windshield_done
                })
            
            work = WorkDone.objects.create(
                worker=worker,
                work_type='tonirovka',
                tonirovka=tonirovka,
                car_name=car_name,
                selected_parts=selected_parts,
                rear_door_count=rear_door,
                front_door_count=front_door,
                rear_windshield_count=rear_windshield,
                front_windshield_count=front_windshield,
                total_price=0,
                worker_share=0
            )
            
            messages.success(request, f"✅ Tonirovka ishi qo'shildi! Admin tasdiqlashi kerak.")
            return redirect('worker_dashboard')
    else:
        form = TonirovkaWorkForm(initial={'worker': request.user.worker})
    
    return render(request, 'worker_panel/tonirovka_form.html', {'form': form})

@worker_required
def sonsa_work(request):
    if request.method == 'POST':
        form = SonsaWorkForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            sonsa = form.cleaned_data['sonsa']
            car_name = form.cleaned_data['car_name']
            
            # Uvol qiymatlari
            rear_door = form.cleaned_data['rear_door']
            front_door = form.cleaned_data['front_door']
            rear_windshield = form.cleaned_data['rear_windshield']
            front_windshield = form.cleaned_data['front_windshield']
            
            # Checkbox qiymatlari (qaysi qismlar ishlangan)
            rear_door_done = request.POST.get('rear_door_done') == 'on'
            front_door_done = request.POST.get('front_door_done') == 'on'
            rear_windshield_done = request.POST.get('rear_windshield_done') == 'on'
            front_windshield_done = request.POST.get('front_windshield_done') == 'on'
            
            # Tanlangan qismlarni JSON formatda saqlash
            selected_parts = []
            
            if rear_door_done or rear_door > 0:
                selected_parts.append({
                    'key': 'rear_door', 
                    'name': 'Orqa eshik', 
                    'count': rear_door, 
                    'done': rear_door_done
                })
            
            if front_door_done or front_door > 0:
                selected_parts.append({
                    'key': 'front_door', 
                    'name': 'Oldi eshik', 
                    'count': front_door, 
                    'done': front_door_done
                })
            
            if rear_windshield_done or rear_windshield > 0:
                selected_parts.append({
                    'key': 'rear_windshield', 
                    'name': 'Orqa lobovoy', 
                    'count': rear_windshield, 
                    'done': rear_windshield_done
                })
            
            if front_windshield_done or front_windshield > 0:
                selected_parts.append({
                    'key': 'front_windshield', 
                    'name': 'Oldi lobovoy', 
                    'count': front_windshield, 
                    'done': front_windshield_done
                })
            
            work = WorkDone.objects.create(
                worker=worker,
                work_type='sonsa',
                sonsa=sonsa,
                car_name=car_name,
                selected_parts=selected_parts,
                rear_door_count=rear_door,
                front_door_count=front_door,
                rear_windshield_count=rear_windshield,
                front_windshield_count=front_windshield,
                total_price=0,
                worker_share=0
            )
            
            messages.success(request, f"✅ Sonsa zashita ishi qo'shildi! Admin tasdiqlashi kerak.")
            return redirect('worker_dashboard')
    else:
        form = SonsaWorkForm(initial={'worker': request.user.worker})
    
    return render(request, 'worker_panel/sonsa_form.html', {'form': form})

@worker_required
def laminatsiya_work(request):
    if request.method == 'POST':
        form = LaminationWorkForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            film = form.cleaned_data['lamination_film']
            car_name = form.cleaned_data['car_name']
            meters = form.cleaned_data['meters_used']
            
            total = meters * film.price_per_meter
            worker_share = total * worker.salary_percent / 100
            
            work = WorkDone.objects.create(
                worker=worker,
                work_type='laminatsiya',
                lamination_film=film,
                car_name=car_name,
                is_detailed=form.cleaned_data['is_detailed'] == 'true',
                meters_used=meters,
                total_price=total,
                worker_share=worker_share,
                is_confirmed=True,
                confirmed_at=timezone.now()
            )
            
            worker.current_salary += worker_share
            worker.save()
            
            messages.success(request, f"✅ Laminatsiya ishi qo'shildi! Sizning ulushingiz: {worker_share} so'm")
            return redirect('worker_dashboard')
    else:
        form = LaminationWorkForm(initial={'worker': request.user.worker})
    
    return render(request, 'worker_panel/laminatsiya_form.html', {'form': form})

@worker_required
def bron_work(request):
    if request.method == 'POST':
        form = BronWorkForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            film = form.cleaned_data['protective_film']
            car_name = form.cleaned_data['car_name']
            meters = form.cleaned_data['meters_used']
            
            # Eski qismlar (dona)
            rear_door = form.cleaned_data.get('rear_door', 0)
            front_door = form.cleaned_data.get('front_door', 0)
            rear_windshield = form.cleaned_data.get('rear_windshield', 0)
            front_windshield = form.cleaned_data.get('front_windshield', 0)
            hood = form.cleaned_data.get('hood', 0)
            trunk = form.cleaned_data.get('trunk', 0)
            roof = form.cleaned_data.get('roof', 0)
            bumper = form.cleaned_data.get('bumper', 0)
            other = form.cleaned_data.get('other', 0)
            other_name = form.cleaned_data.get('other_name', '')
            
            # Yangi text maydoni
            done_parts_text = request.POST.get('done_parts_text', '')
            
            # Tanlangan qismlarni JSON formatda saqlash (dona)
            selected_parts = []
            if rear_door > 0:
                selected_parts.append({'key': 'rear_door', 'name': 'Orqa eshik', 'count': rear_door})
            if front_door > 0:
                selected_parts.append({'key': 'front_door', 'name': 'Oldi eshik', 'count': front_door})
            if rear_windshield > 0:
                selected_parts.append({'key': 'rear_windshield', 'name': 'Orqa lobovoy', 'count': rear_windshield})
            if front_windshield > 0:
                selected_parts.append({'key': 'front_windshield', 'name': 'Oldi lobovoy', 'count': front_windshield})
            if hood > 0:
                selected_parts.append({'key': 'hood', 'name': 'Kapot', 'count': hood})
            if trunk > 0:
                selected_parts.append({'key': 'trunk', 'name': 'Bakajnik', 'count': trunk})
            if roof > 0:
                selected_parts.append({'key': 'roof', 'name': 'Tom', 'count': roof})
            if bumper > 0:
                selected_parts.append({'key': 'bumper', 'name': 'Bamper', 'count': bumper})
            if other > 0:
                selected_parts.append({'key': 'other', 'name': other_name or 'Boshqa', 'count': other})
            
            # Text ma'lumotni ham qo'shamiz
            if done_parts_text:
                selected_parts.append({
                    'key': 'text_description',
                    'name': 'Matnli izoh',
                    'description': done_parts_text
                })
            
            total = meters * film.price_per_meter
            worker_share = total * worker.salary_percent / 100
            
            work = WorkDone.objects.create(
                worker=worker,
                work_type='bron',
                protective_film=film,
                car_name=car_name,
                selected_parts=selected_parts,
                meters_used=meters,
                rear_door_count=rear_door,
                front_door_count=front_door,
                rear_windshield_count=rear_windshield,
                front_windshield_count=front_windshield,
                hood_count=hood,
                trunk_count=trunk,
                roof_count=roof,
                bumper_count=bumper,
                other_count=other,
                other_part_name=other_name if other > 0 else '',
                total_price=total,
                worker_share=worker_share,
                is_confirmed=True,
                confirmed_at=timezone.now()
            )
            
            worker.current_salary += worker_share
            worker.save()
            
            messages.success(request, f"✅ Bron ishi qo'shildi! Sizning ulushingiz: {worker_share} so'm")
            return redirect('worker_dashboard')
    else:
        form = BronWorkForm(initial={'worker': request.user.worker})
    
    return render(request, 'worker_panel/bron_form.html', {'form': form})

# -------------------- Admin: Worker deletion --------------------

@admin_required
def delete_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == 'POST':
        worker.user.delete()
        worker.delete()
        messages.success(request, f"{worker.full_name} o'chirildi.")
        return redirect('workers_list')
    return render(request, 'admin_panel/delete_worker_confirm.html', {'worker': worker})





def check_three_hour_bonus(worker, session):
    """3 soatdan keyin bonus qo'shish"""
    from django.utils import timezone
    from datetime import timedelta
    
    if not session.check_out and worker.three_hour_bonus_amount > 0:
        now = timezone.now()
        check_in = session.check_in
        interval_hours = 3
        interval_seconds = interval_hours * 3600
        
        # Necha interval o'tgan
        seconds_passed = (now - check_in).total_seconds()
        current_blocks = session.three_hour_bonus_blocks or 0
        new_blocks = int(seconds_passed // interval_seconds)
        
        if new_blocks > current_blocks:
            add_blocks = new_blocks - current_blocks
            bonus_amount = worker.three_hour_bonus_amount * add_blocks
            
            session.three_hour_bonus_blocks = new_blocks
            session.three_hour_total_bonus = (session.three_hour_total_bonus or 0) + bonus_amount
            session.last_bonus_check = now
            session.save()
            
            worker.total_bonuses += bonus_amount
            worker.save()
            
            return True, bonus_amount, new_blocks, add_blocks
    return False, 0, 0, 0



from datetime import datetime, timedelta

@admin_required
def attendance_list(request):
    from datetime import datetime, timedelta, date
    
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    weekdays = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
    
    week_dates = []
    for i in range(7):
        week_dates.append(week_start + timedelta(days=i))
    
    workers = Worker.objects.all()
    
    attendance_data = []
    for worker in workers:
        worker_data = {
            'worker': worker,
            'days': []
        }
        for day_date in week_dates:  # 'date' o'rniga 'day_date' ishlatildi
            session = WorkSession.objects.filter(
                worker=worker,
                check_in__date=day_date
            ).first()
            worker_data['days'].append({
                'date': day_date,
                'weekday': weekdays[day_date.weekday()],
                'check_in': session.check_in if session else None,
                'check_out': session.check_out if session else None,
                'session_id': session.id if session else None,
                'has_session': session is not None
            })
        attendance_data.append(worker_data)
    
    context = {
        'attendance_data': attendance_data,
        'week_dates': week_dates,
        'weekdays': weekdays,
        'week_start': week_start,
        'week_end': week_end,
    }
    return render(request, 'admin_panel/attendance_list.html', context)

@admin_required
def attendance_edit(request, session_id):
    """Davomat vaqtini tahrirlash"""
    session = get_object_or_404(WorkSession, id=session_id)
    
    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_in_time = request.POST.get('check_in_time')
        check_out_date = request.POST.get('check_out_date')
        check_out_time = request.POST.get('check_out_time')
        
        # Kelgan vaqtni yangilash
        if check_in_date and check_in_time:
            check_in_datetime = datetime.strptime(f"{check_in_date} {check_in_time}", "%Y-%m-%d %H:%M")
            check_in_datetime = timezone.make_aware(check_in_datetime)
            session.check_in = check_in_datetime
        
        # Ketgan vaqtni yangilash
        if check_out_date and check_out_time:
            check_out_datetime = datetime.strptime(f"{check_out_date} {check_out_time}", "%Y-%m-%d %H:%M")
            check_out_datetime = timezone.make_aware(check_out_datetime)
            session.check_out = check_out_datetime
        else:
            session.check_out = None
        
        session.save()
        messages.success(request, f"{session.worker.full_name} ning davomati yangilandi!")
        return redirect('attendance_list')
    
    context = {
        'session': session,
        'worker': session.worker,
        'check_in': session.check_in,
        'check_out': session.check_out,
    }
    return render(request, 'admin_panel/attendance_edit.html', context)


@admin_required
def attendance_create(request, worker_id, date):
    """Yangi davomat yaratish (agar ishchi kelmagan bo'lsa)"""
    worker = get_object_or_404(Worker, id=worker_id)
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    
    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_in_time = request.POST.get('check_in_time')
        check_out_date = request.POST.get('check_out_date')
        check_out_time = request.POST.get('check_out_time')
        
        check_in_datetime = None
        check_out_datetime = None
        
        if check_in_date and check_in_time:
            check_in_datetime = datetime.strptime(f"{check_in_date} {check_in_time}", "%Y-%m-%d %H:%M")
            check_in_datetime = timezone.make_aware(check_in_datetime)
        
        if check_out_date and check_out_time:
            check_out_datetime = datetime.strptime(f"{check_out_date} {check_out_time}", "%Y-%m-%d %H:%M")
            check_out_datetime = timezone.make_aware(check_out_datetime)
        
        session = WorkSession.objects.create(
            worker=worker,
            check_in=check_in_datetime,
            check_out=check_out_datetime,
            check_in_lat=0,
            check_in_lng=0,
            is_late=False,
            fine_amount=0,
            is_off_day=False
        )
        
        messages.success(request, f"{worker.full_name} uchun {date_obj} kuni davomat qo'shildi!")
        return redirect('attendance_list')
    
    context = {
        'worker': worker,
        'date': date_obj,
    }
    return render(request, 'admin_panel/attendance_create.html', context)





@admin_required
def add_car(request):
    """Admin panelda mashina qo'shish"""
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            
            # Standart qismlarni qo'shish
            part_names = request.POST.getlist('part_name[]')
            for name in part_names:
                if name.strip():
                    CarPart.objects.create(car=car, name=name.strip(), is_default=True)
            
            messages.success(request, f"{car.name} mashinasi qo'shildi!")
            return redirect('cars_list')
    else:
        form = CarForm()
    
    return render(request, 'admin_panel/add_car.html', {'form': form})


@admin_required
def cars_list(request):
    """Mashinalar ro'yxati"""
    cars = Car.objects.all()
    return render(request, 'admin_panel/cars_list.html', {'cars': cars})


@worker_required
def worker_add_car_work(request, car_id):
    """Tanlangan mashinaga ish qo'shish (avtomatik tasdiqlanadi)"""
    from datetime import date
    from django.utils import timezone
    from django.contrib.auth.models import User
    
    car = get_object_or_404(Car, id=car_id)
    
    # Hali bajarilmagan qismlar
    pending_parts = car.get_pending_parts()
    
    if not pending_parts.exists():
        messages.error(request, f"{car.name} mashinasining barcha qismlari allaqachon bajarilgan!")
        return redirect('work_done')
    
    if request.method == 'POST':
        worker_name = request.POST.get('worker_name', '').strip()
        
        if not worker_name:
            messages.error(request, "Ishchi ismini yozing!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        # User yaratish (username sifatida ismni olib)
        username = worker_name.replace(' ', '_').lower()
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={'password': '123456'}
        )
        
        # Ishchini topish yoki yaratish
        worker, created = Worker.objects.get_or_create(
            full_name=worker_name,
            defaults={
                'user': user,
                'salary_percent': 0,
                'late_fine': 0,
                'overtime_bonus': 0
            }
        )
        
        # Agar ishchi mavjud bo'lsa, user'ni yangilash
        if not created and worker.user is None:
            worker.user = user
            worker.save()
        
        # Tanlangan qismlar
        selected_part_ids = request.POST.getlist('selected_parts[]')
        
        if not selected_part_ids:
            messages.error(request, "Kamida bitta qismni tanlang!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        added_count = 0
        
        for part_id in selected_part_ids:
            part = CarPart.objects.get(id=part_id)
            
            car_work = CarWork.objects.create(
                car=car,
                worker=worker,
                work_type='other',
                work_date=date.today(),
                total_price=0,
                worker_share=0,
                is_confirmed=True,
                confirmed_at=timezone.now()
            )
            
            CarWorkPart.objects.create(
                car_work=car_work,
                part=part,
                count=1
            )
            added_count += 1
        
        if car.check_completion():
            messages.success(request, f"✅ {car.name} mashinasining BARCHA qismlari bajarildi!")
        else:
            remaining = car.get_pending_parts().count()
            messages.success(request, f"✅ {car.name} mashinasiga {added_count} ta qism qo'shildi. Yana {remaining} ta qism qoldi.")
        
        return redirect('work_done')
    
    context = {
        'car': car,
        'pending_count': pending_parts.count(),
        'pending_parts': pending_parts
    }
    return render(request, 'worker_panel/add_car_work.html', context)

@worker_required
def worker_add_car_work(request, car_id):
    """Tanlangan mashinaga ish qo'shish (avtomatik tasdiqlanadi)"""
    from datetime import date
    from django.utils import timezone
    
    car = get_object_or_404(Car, id=car_id)
    
    # Hali bajarilmagan qismlar
    pending_parts = car.get_pending_parts()
    
    if not pending_parts.exists():
        messages.error(request, f"{car.name} mashinasining barcha qismlari allaqachon bajarilgan!")
        return redirect('work_done')
    
    if request.method == 'POST':
        worker_name = request.POST.get('worker_name', '').strip()
        
        if not worker_name:
            messages.error(request, "Ishchi ismini yozing!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        # Ishchini topish yoki yaratish
        worker, created = Worker.objects.get_or_create(
            full_name=worker_name,
            defaults={
                'user': None,
                'salary_percent': 0,
                'late_fine': 0,
                'overtime_bonus': 0
            }
        )
        
        # Checkbox bilan tanlangan qismlar
        selected_part_ids = request.POST.getlist('selected_parts[]')
        
        # Text field bilan yozilgan uvol joylari
        uvol_text = request.POST.get('uvol_text', '').strip()
        
        if not selected_part_ids and not uvol_text:
            messages.error(request, "Kamida bitta qismni tanlang yoki uvol joylarini yozing!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        added_count = 0
        
        # Checkbox bilan tanlangan qismlarni qo'shish
        for part_id in selected_part_ids:
            part = CarPart.objects.get(id=part_id)
            
            car_work = CarWork.objects.create(
                car=car,
                worker=worker,
                work_type='other',
                work_date=date.today(),
                total_price=0,
                worker_share=0,
                is_confirmed=True,
                confirmed_at=timezone.now()
            )
            
            CarWorkPart.objects.create(
                car_work=car_work,
                part=part,
                count=1
            )
            added_count += 1
        
        # Text field bilan yozilgan uvol joylarini qo'shish
        if uvol_text:
            part_names = [p.strip() for p in uvol_text.split(',') if p.strip()]
            for part_name in part_names:
                if part_name:
                    # Qismni topish yoki yaratish
                    part, created = CarPart.objects.get_or_create(
                        car=car,
                        name=part_name,
                        defaults={'is_default': True}
                    )
                    
                    car_work = CarWork.objects.create(
                        car=car,
                        worker=worker,
                        work_type='other',
                        work_date=date.today(),
                        total_price=0,
                        worker_share=0,
                        is_confirmed=True,
                        confirmed_at=timezone.now()
                    )
                    
                    CarWorkPart.objects.create(
                        car_work=car_work,
                        part=part,
                        count=1
                    )
                    added_count += 1
        
        # Mashinaning barcha qismlari bajarilganligini tekshirish
        if car.check_completion():
            messages.success(request, f"✅ {car.name} mashinasining BARCHA qismlari bajarildi!")
        else:
            remaining = car.get_pending_parts().count()
            messages.success(request, f"✅ {car.name} mashinasiga {added_count} ta qism qo'shildi. Yana {remaining} ta qism qoldi.")
        
        return redirect('work_done')
    
    context = {
        'car': car,
        'pending_count': pending_parts.count(),
        'pending_parts': pending_parts
    }
    return render(request, 'worker_panel/add_car_work.html', context)



def api_car_parts(request):
    """Mashina qismlarini JSON formatda qaytarish"""
    car_id = request.GET.get('car_id')
    if car_id:
        car = Car.objects.get(id=car_id)
        # Faqat bajarilmagan qismlarni qaytarish
        pending_parts = car.get_pending_parts()
        parts = pending_parts.values('id', 'name')
        return JsonResponse({
            'parts': list(parts),
            'is_completed': car.is_completed
        })
    return JsonResponse({'parts': [], 'is_completed': False})

@admin_required
def add_car_work_admin(request):
    """Admin panelda ish qo'shish (ishchi tanlanmaydi, worker panelda ko'rinadi)"""
    from datetime import datetime, date
    
    if request.method == 'POST':
        car_name = request.POST.get('car_name', '').strip()
        
        print("=" * 60)
        print(f"ADD_CAR_WORK_ADMIN - Mashina: {car_name}")
        
        if not car_name:
            messages.error(request, "Mashina nomini kiriting!")
            return redirect('add_car_work_admin')
        
        owner_phone = request.POST.get('owner_phone', '').strip()
        work_date_str = request.POST.get('work_date', '')
        
        if work_date_str:
            try:
                work_date = datetime.strptime(work_date_str, '%Y-%m-%d').date()
            except:
                work_date = date.today()
        else:
            work_date = date.today()
        
        # Mashinani topish yoki yaratish
        car, created = Car.objects.get_or_create(
            name=car_name,
            defaults={'owner_phone': owner_phone}
        )
        print(f"Mashina: {car.name}, Yangi yaratildi: {created}")
        
        if owner_phone:
            car.owner_phone = owner_phone
            car.save()
        
        # Qismlarni olish
        part_names = request.POST.getlist('part_name[]')
        print(f"Qismlar: {part_names}")
        
        added_parts = []
        for name in part_names:
            if name.strip():
                part, created = CarPart.objects.get_or_create(
                    car=car,
                    name=name.strip(),
                    defaults={'is_default': True}
                )
                added_parts.append(part)
                print(f"Qism qo'shildi: {part.name}, Yangi: {created}")
        
        if not added_parts:
            messages.error(request, "Kamida bitta qism nomini kiriting!")
            return redirect('add_car_work_admin')
        
        # Ishni saqlash (worker=None, is_confirmed=False)
        car_work = CarWork.objects.create(
            car=car,
            worker=None,
            work_type='other',
            work_date=work_date,
            total_price=0,
            worker_share=0,
            is_confirmed=False,
            confirmed_at=None
        )
        print(f"Ish yaratildi: ID={car_work.id}, worker=None, is_confirmed=False")
        
        for part in added_parts:
            CarWorkPart.objects.create(
                car_work=car_work,
                part=part,
                count=1
            )
            print(f"Bajarilgan qism qo'shildi: {part.name}")
        
        messages.success(request, f"✅ {car_name} mashinasiga ish qo'shildi!")
        return redirect('admin_dashboard')
    
    return render(request, 'admin_panel/add_car_work.html')
@worker_required
def worker_add_car_work(request, car_id):
    """Tanlangan mashinaga ish qo'shish (avtomatik tasdiqlanadi)"""
    car = get_object_or_404(Car, id=car_id)
    
    # Hali bajarilmagan qismlar
    pending_parts = car.get_pending_parts()
    
    if not pending_parts.exists():
        messages.error(request, f"{car.name} mashinasining barcha qismlari allaqachon bajarilgan!")
        return redirect('work_done')
    
    if request.method == 'POST':
        # Tanlangan ishchi
        worker_id = request.POST.get('worker_id')
        worker = get_object_or_404(Worker, id=worker_id) if worker_id else None
        
        if not worker:
            messages.error(request, "Ishchini tanlang!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        # Checkbox bilan tanlangan qismlar
        selected_part_ids = request.POST.getlist('selected_parts[]')
        
        # Text field bilan yozilgan uvol joylari
        uvol_text = request.POST.get('uvol_text', '').strip()
        
        # Hech narsa tanlanmagan bo'lsa
        if not selected_part_ids and not uvol_text:
            messages.error(request, "Kamida bitta qismni tanlang yoki uvol joylarini yozing!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        # Checkbox bilan tanlangan qismlarni qo'shish
        for part_id in selected_part_ids:
            part = CarPart.objects.get(id=part_id)
            
            car_work = CarWork.objects.create(
                car=car,
                worker=worker,
                work_type='other',
                work_date=date.today(),
                total_price=0,
                worker_share=0,
                is_confirmed=True,
                confirmed_at=timezone.now()
            )
            
            CarWorkPart.objects.create(car_work=car_work, part=part, count=1)
        
        # Text field bilan yozilgan uvol joylarini qo'shish
        if uvol_text:
            # Qismlarni vergul bilan ajratib olish
            part_names = [p.strip() for p in uvol_text.split(',') if p.strip()]
            
            for part_name in part_names:
                part, created = CarPart.objects.get_or_create(
                    car=car,
                    name=part_name,
                    defaults={'is_default': True}
                )
                
                car_work = CarWork.objects.create(
                    car=car,
                    worker=worker,
                    work_type='other',
                    work_date=date.today(),
                    total_price=0,
                    worker_share=0,
                    is_confirmed=True,
                    confirmed_at=timezone.now()
                )
                
                CarWorkPart.objects.create(car_work=car_work, part=part, count=1)
        
        # Mashinaning barcha qismlari bajarilganligini tekshirish
        if car.check_completion():
            messages.success(request, f"✅ {car.name} mashinasining BARCHA qismlari bajarildi!")
        else:
            remaining = car.get_pending_parts().count()
            messages.success(request, f"✅ {car.name} mashinasiga ish qo'shildi. Yana {remaining} ta qism qoldi.")
        
        return redirect('work_done')
    
    # Barcha ishchilar
    workers = Worker.objects.all()
    
    context = {
        'car': car,
        'workers': workers,
        'pending_count': pending_parts.count(),
        'pending_parts': pending_parts
    }
    return render(request, 'worker_panel/add_car_work.html', context)

@admin_required
def pending_car_works(request):
    """Tasdiqlanmagan ishlar ro'yxati"""
    pending_works = CarWork.objects.filter(is_confirmed=False).order_by('-created_at')
    return render(request, 'admin_panel/pending_car_works.html', {'pending_works': pending_works})


@admin_required
def confirm_car_work(request, work_id):
    """Ishni tasdiqlash va narx kiritish"""
    car_work = get_object_or_404(CarWork, id=work_id)
    
    if request.method == 'POST':
        total_price = request.POST.get('total_price', 0)
        try:
            total_price = float(total_price)
        except:
            total_price = 0
        
        worker_share = total_price * car_work.worker.salary_percent / 100
        
        car_work.total_price = total_price
        car_work.worker_share = worker_share
        car_work.is_confirmed = True
        car_work.confirmed_at = timezone.now()
        car_work.save()
        
        car_work.worker.current_salary += worker_share
        car_work.worker.save()
        
        car_work.car.check_completion()
        
        messages.success(request, f"{car_work.car.name} mashinasidagi ish tasdiqlandi! Ishchi ulushi: {worker_share} so'm")
        return redirect('pending_car_works')
    
    context = {
        'car_work': car_work,
        'worker': car_work.worker,
        'car': car_work.car,
        'parts': car_work.completed_parts.all()
    }
    return render(request, 'admin_panel/confirm_car_work.html', context)


@admin_required
def add_car_work_admin(request):
    """Admin panelda ish qo'shish (har doim yangi mashina va qismlar yaratiladi)"""
    from datetime import datetime, date
    
    if request.method == 'POST':
        car_name = request.POST.get('car_name', '').strip()
        
        if not car_name:
            messages.error(request, "Mashina nomini kiriting!")
            return redirect('add_car_work_admin')
        
        owner_phone = request.POST.get('owner_phone', '').strip()
        work_date_str = request.POST.get('work_date', '')
        
        if work_date_str:
            try:
                work_date = datetime.strptime(work_date_str, '%Y-%m-%d').date()
            except:
                work_date = date.today()
        else:
            work_date = date.today()
        
        # HAR DOIM YANGI MASHINA YARATISH
        car = Car.objects.create(
            name=car_name,
            owner_phone=owner_phone
        )
        
        # Qismlarni yaratish (HAR DOIM YANGI)
        part_names = request.POST.getlist('part_name[]')
        
        for name in part_names:
            if name.strip():
                CarPart.objects.create(
                    car=car,
                    name=name.strip(),
                    is_default=True
                )
        
        messages.success(request, f"✅ {car_name} mashinasiga yangi ish qo'shildi! Worker panelda ko'rinadi.")
        return redirect('admin_dashboard')
    
    return render(request, 'admin_panel/add_car_work.html')



@admin_required
def add_car(request):
    """Admin panelda mashina qo'shish"""
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            
            part_names = request.POST.getlist('part_name[]')
            for name in part_names:
                if name.strip():
                    CarPart.objects.create(car=car, name=name.strip(), is_default=True)
            
            messages.success(request, f"{car.name} mashinasi qo'shildi!")
            return redirect('cars_list')
    else:
        form = CarForm()
    
    return render(request, 'admin_panel/add_car.html', {'form': form})


@admin_required
def cars_list(request):
    """Mashinalar ro'yxati"""
    cars = Car.objects.all()
    return render(request, 'admin_panel/cars_list.html', {'cars': cars})


@worker_required
def worker_add_car_work(request, car_id):
    """Tanlangan mashinaga ish qo'shish (avtomatik tasdiqlanadi)"""
    from datetime import date
    from django.utils import timezone
    from django.contrib.auth.models import User
    
    car = get_object_or_404(Car, id=car_id)
    
    # Hali bajarilmagan qismlar
    pending_parts = car.get_pending_parts()
    
    if not pending_parts.exists():
        messages.error(request, f"{car.name} mashinasining barcha qismlari allaqachon bajarilgan!")
        return redirect('work_done')
    
    if request.method == 'POST':
        # POST so'rovi uchun
        worker_name = request.POST.get('worker_name', '').strip()
        
        if not worker_name:
            messages.error(request, "Ishchi ismini yozing!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        # User yaratish
        username = worker_name.replace(' ', '_').lower()
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={'password': '123456'}
        )
        
        # Ishchini topish yoki yaratish
        worker, created = Worker.objects.get_or_create(
            full_name=worker_name,
            defaults={
                'user': user,
                'salary_percent': 0,
                'late_fine': 0,
                'overtime_bonus': 0
            }
        )
        
        if not created and worker.user is None:
            worker.user = user
            worker.save()
        
        # Tanlangan qismlar
        selected_part_ids = request.POST.getlist('selected_parts[]')
        
        if not selected_part_ids:
            messages.error(request, "Kamida bitta qismni tanlang!")
            return redirect('worker_add_car_work', car_id=car_id)
        
        added_count = 0
        
        for part_id in selected_part_ids:
            part = CarPart.objects.get(id=part_id)
            
            car_work = CarWork.objects.create(
                car=car,
                worker=worker,
                work_type='other',
                work_date=date.today(),
                total_price=0,
                worker_share=0,
                is_confirmed=True,
                confirmed_at=timezone.now()
            )
            
            CarWorkPart.objects.create(
                car_work=car_work,
                part=part,
                count=1
            )
            added_count += 1
        
        if car.check_completion():
            messages.success(request, f"✅ {car.name} mashinasining BARCHA qismlari bajarildi!")
        else:
            remaining = car.get_pending_parts().count()
            messages.success(request, f"✅ {car.name} mashinasiga {added_count} ta qism qo'shildi. Yana {remaining} ta qism qoldi.")
        
        return redirect('work_done')
    
    # GET so'rovi uchun (worker_name ishlatilmaydi)
    context = {
        'car': car,
        'pending_count': pending_parts.count(),
        'pending_parts': pending_parts
    }
    return render(request, 'worker_panel/add_car_work.html', context)

def api_car_parts(request):
    """Mashina qismlarini JSON formatda qaytarish"""
    car_id = request.GET.get('car_id')
    if car_id:
        completed_by_anyone = CarWorkPart.objects.filter(
            car_work__car_id=car_id,
            car_work__is_confirmed=True
        ).values_list('part_id', flat=True)
        
        parts = CarPart.objects.filter(car_id=car_id).exclude(id__in=completed_by_anyone).values('id', 'name')
        return JsonResponse({'parts': list(parts)})
    return JsonResponse({'parts': []})


from .models import Worker

@worker_required
def work_done(request):
    """Ish qo'shish sahifasi - barcha mashinalar (faqat ishlanmaganlar)"""
    # Barcha mashinalar
    all_cars = Car.objects.all()
    
    print("=" * 60)
    print("WORK_DONE - Barcha mashinalar")
    
    available_cars = []
    for car in all_cars:
        print(f"\n--- Mashina: {car.name} ---")
        
        # Barcha qismlar
        all_parts = car.parts.all()
        print(f"Barcha qismlar: {[p.name for p in all_parts]}")
        
        # Bajarilgan qismlarni hisoblash
        completed_parts = CarWorkPart.objects.filter(
            car_work__car=car
        ).values_list('part_id', flat=True)
        print(f"Bajarilgan qismlar ID: {list(completed_parts)}")
        
        # Bajarilmagan qismlar
        pending_parts = all_parts.exclude(id__in=completed_parts)
        print(f"Bajarilmagan qismlar: {[p.name for p in pending_parts]}")
        print(f"Bajarilmagan qismlar soni: {pending_parts.count()}")
        
        if pending_parts.exists():
            available_cars.append({
                'car': car,
                'pending_count': pending_parts.count()
            })
            print(f"✅ Qo'shildi: {car.name}")
        else:
            print(f"❌ Qo'shilmadi: {car.name} (barcha qismlar bajarilgan)")
    
    print(f"\nJami ko'rsatiladigan mashinalar: {len(available_cars)}")
    print("=" * 60)
    
    return render(request, 'worker_panel/work_done.html', {
        'available_cars': available_cars
    })
    
@admin_required
def work_history(request):
    """Ishlar tarixi - yil va oy bo'yicha filtr"""
    from datetime import date
    from django.db.models import Count, Sum
    
    # Yillar ro'yxati (2020 dan hozirgi yilgacha)
    current_year = date.today().year
    years = range(2020, current_year + 1)
    
    # Tanlangan yil va oy
    selected_year = request.GET.get('year', current_year)
    selected_month = request.GET.get('month', date.today().month)
    
    try:
        selected_year = int(selected_year)
        selected_month = int(selected_month)
    except:
        selected_year = current_year
        selected_month = date.today().month
    
    # Tanlangan oy va yil uchun ishlar
    works = CarWork.objects.filter(
        work_date__year=selected_year,
        work_date__month=selected_month,
        is_confirmed=True
    ).order_by('-work_date')
    
    # Oylar ro'yxati
    months = [
        (1, 'Yanvar'), (2, 'Fevral'), (3, 'Mart'), (4, 'Aprel'),
        (5, 'May'), (6, 'Iyun'), (7, 'Iyul'), (8, 'Avgust'),
        (9, 'Sentabr'), (10, 'Oktabr'), (11, 'Noyabr'), (12, 'Dekabr')
    ]
    
    # Har bir ish uchun qismlar ma'lumotini olish
    work_list = []
    for work in works:
        parts_list = []
        for part in work.completed_parts.all():
            parts_list.append(part.part.name)
        
        work_list.append({
            'date': work.work_date,
            'car': work.car.name,
            'worker': work.worker.full_name if work.worker else 'Noma\'lum',
            'parts': ', '.join(parts_list) if parts_list else work.car.get_pending_parts_count(),
            'total_price': work.total_price
        })
    
    # Diagramma uchun statistikalar
    # 1. Har bir ishchi bo'yicha ishlar soni
    worker_stats = CarWork.objects.filter(
        work_date__year=selected_year,
        work_date__month=selected_month,
        is_confirmed=True
    ).values('worker__full_name').annotate(
        count=Count('id'),
        total_sum=Sum('total_price')
    ).order_by('-count')
    
    # 2. Har bir mashina bo'yicha ishlar soni
    car_stats = CarWork.objects.filter(
        work_date__year=selected_year,
        work_date__month=selected_month,
        is_confirmed=True
    ).values('car__name').annotate(
        count=Count('id'),
        total_sum=Sum('total_price')
    ).order_by('-count')
    
    context = {
        'works': work_list,
        'years': years,
        'months': months,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'selected_month_name': dict(months).get(selected_month, ''),
        'worker_stats': list(worker_stats),
        'car_stats': list(car_stats),
        'total_works': len(work_list),
        'total_amount': sum(w['total_price'] for w in work_list if w['total_price']),
    }
    return render(request, 'admin_panel/work_history.html', context)