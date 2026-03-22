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
            if overtime_minutes >= 30:
                full_blocks = overtime_minutes // 30
                bonus = (full_blocks * worker.overtime_bonus) / 2
            
            session.overtime_minutes = overtime_minutes
            session.bonus_amount = bonus
            
            if bonus > 0:
                worker.total_bonuses += bonus
                worker.save()
        
        session.save()
        
        if bonus > 0:
            hours = overtime_minutes // 60
            half_hours = (overtime_minutes % 60) // 30
            msg = f"Ketishingiz belgilandi! Qo'shimcha ish: {overtime_minutes} daqiqa. "
            if hours > 0:
                msg += f"{hours} soat "
            if half_hours > 0:
                msg += f"{half_hours*30} daqiqa "
            msg += f"uchun bonus: {bonus} so'm"
            messages.success(request, msg)
        else:
            if overtime_minutes > 0:
                messages.info(
                    request, 
                    f"Ketishingiz belgilandi! {overtime_minutes} daqiqa qo'shimcha ishlagansiz, "
                    f"lekin 30 daqiqa to'lmagani uchun bonus yo'q."
                )
            else:
                messages.success(request, "Ketishingiz belgilandi!")
    
    return redirect('worker_dashboard')

@worker_required
def work_done(request):
    return render(request, 'worker_panel/work_done.html')

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