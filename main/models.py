from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import time
from django.utils import timezone

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')
    full_name = models.CharField(max_length=255, verbose_name="To'liq ismi")
    salary_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Oylik foizi (%)")
    late_fine = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="10 min kechiksa jarima (so'm)")
    overtime_bonus = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="1 soat qo'shimcha bonus (so'm)")
    
    # Haftalik ish vaqti (vaqt maydonlari)
    monday_start = models.TimeField(default=time(9, 0))
    monday_end = models.TimeField(default=time(18, 0))
    tuesday_start = models.TimeField(default=time(9, 0))
    tuesday_end = models.TimeField(default=time(18, 0))
    wednesday_start = models.TimeField(default=time(9, 0))
    wednesday_end = models.TimeField(default=time(18, 0))
    thursday_start = models.TimeField(default=time(9, 0))
    thursday_end = models.TimeField(default=time(18, 0))
    friday_start = models.TimeField(default=time(9, 0))
    friday_end = models.TimeField(default=time(18, 0))
    saturday_start = models.TimeField(default=time(9, 0))
    saturday_end = models.TimeField(default=time(18, 0))
    sunday_start = models.TimeField(default=time(9, 0))
    sunday_end = models.TimeField(default=time(18, 0))
    
    # Qaysi kunlar ish kuni ekanligi (checkbox)
    monday_working = models.BooleanField(default=True, verbose_name="Dushanba ish kuni")
    tuesday_working = models.BooleanField(default=True, verbose_name="Seshanba ish kuni")
    wednesday_working = models.BooleanField(default=True, verbose_name="Chorshanba ish kuni")
    thursday_working = models.BooleanField(default=True, verbose_name="Payshanba ish kuni")
    friday_working = models.BooleanField(default=True, verbose_name="Juma ish kuni")
    saturday_working = models.BooleanField(default=True, verbose_name="Shanba ish kuni")
    sunday_working = models.BooleanField(default=True, verbose_name="Yakshanba ish kuni")
    
    # Hisob-kitob maydonlari
    current_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_fines = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_bonuses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    three_hour_bonus_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="3 soatdan keyin bonus (so'm)"
    )
    
    

    
    def __str__(self):
        return self.full_name
    
    def net_salary(self):
        """Sof oylik (joriy oylik + bonuslar - jarimalar)"""
        return self.current_salary + self.total_bonuses - self.total_fines
    
    def remaining_debt(self):
        """Qolgan qarz (sof oylik - to'langan)"""
        return self.net_salary() - self.total_paid
    
    def reset_monthly(self):
        """Oylikni 0 ga tenglash"""
        self.current_salary = 0
        self.total_fines = 0
        self.total_bonuses = 0
        self.save()
    
    def is_working_day(self, date_obj):
        """Berilgan sana ish kuni ekanligini qaytaradi"""
        weekday = date_obj.weekday()  # 0=dushanba, 6=yakshanba
        if weekday == 0:
            return self.monday_working
        elif weekday == 1:
            return self.tuesday_working
        elif weekday == 2:
            return self.wednesday_working
        elif weekday == 3:
            return self.thursday_working
        elif weekday == 4:
            return self.friday_working
        elif weekday == 5:
            return self.saturday_working
        else:
            return self.sunday_working
    
    class Meta:
        verbose_name = "Ishchi"
        verbose_name_plural = "Ishchilar"


class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} - {self.name or 'Dam olish'}"
    
    class Meta:
        verbose_name = "Dam olish kuni"
        verbose_name_plural = "Dam olish kunlari"


class Tonirovka(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tonirovka"
        verbose_name_plural = "Tonirovkalar"


class SonsaZashita(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sonsa Zashita"
        verbose_name_plural = "Sonsa Zashitalar"


class LaminationFilm(models.Model):
    name = models.CharField(max_length=255)
    price_per_meter = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Laminatsiya plyonkasi"
        verbose_name_plural = "Laminatsiya plyonkalari"


class ProtectiveFilm(models.Model):
    name = models.CharField(max_length=255)
    price_per_meter = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Bron plyonka"
        verbose_name_plural = "Bron plyonkalar"


class WorkSession(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='work_sessions')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    check_in_lat = models.FloatField(null=True, blank=True)
    check_in_lng = models.FloatField(null=True, blank=True)
    check_out_lat = models.FloatField(null=True, blank=True)
    check_out_lng = models.FloatField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_minutes = models.IntegerField(default=0)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_off_day = models.BooleanField(default=False)  # dam olish kunida kelganmi?
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    three_hour_bonus_blocks = models.IntegerField(default=0, verbose_name="3 soatlik bonus bloklari soni")
    three_hour_total_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="3 soatlik jami bonus")
    last_bonus_check = models.DateTimeField(null=True, blank=True, verbose_name="Oxirgi bonus tekshiruvi")
    
    
    
    def __str__(self):
        return f"{self.worker.full_name} - {self.check_in.date()}"
    
    class Meta:
        verbose_name = "Ish seansi"
        verbose_name_plural = "Ish seanslari"
        ordering = ['-check_in']


class WorkDone(models.Model):
    WORK_TYPES = [
        ('tonirovka', 'Tonirovka'),
        ('sonsa', 'Sonsa Zashita'),
        ('laminatsiya', 'Laminatsiya'),
        ('bron', 'Bron'),
    ]
    
    PART_TYPES = [
        ('rear_door', 'Orqa eshik'),
        ('front_door', 'Oldi eshik'),
        ('rear_windshield', 'Orqa lobovoy'),
        ('front_windshield', 'Oldi lobovoy'),
        ('hood', 'Kapot'),
        ('trunk', 'Bakajnik'),
        ('roof', 'Tom'),
        ('bumper', 'Bamper'),
        ('other', 'Boshqa'),
    ]
    
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='works_done')
    work_type = models.CharField(max_length=20, choices=WORK_TYPES)
    date = models.DateField(auto_now_add=True)
    
    # Tanlangan qismlar (JSON formatda saqlanadi)
    selected_parts = models.JSONField(default=list, blank=True)
    
    # Tonirovka va Sonsa uchun
    tonirovka = models.ForeignKey(Tonirovka, on_delete=models.SET_NULL, null=True, blank=True)
    sonsa = models.ForeignKey(SonsaZashita, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Har bir qism uchun alohida sonlar
    rear_door_count = models.IntegerField(default=0)
    front_door_count = models.IntegerField(default=0)
    rear_windshield_count = models.IntegerField(default=0)
    front_windshield_count = models.IntegerField(default=0)
    hood_count = models.IntegerField(default=0)
    trunk_count = models.IntegerField(default=0)
    roof_count = models.IntegerField(default=0)
    bumper_count = models.IntegerField(default=0)
    other_count = models.IntegerField(default=0)
    other_part_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Laminatsiya uchun
    lamination_film = models.ForeignKey(LaminationFilm, on_delete=models.SET_NULL, null=True, blank=True)
    is_detailed = models.BooleanField(default=True)
    meters_used = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Bron uchun
    protective_film = models.ForeignKey(ProtectiveFilm, on_delete=models.SET_NULL, null=True, blank=True)
    car_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Mashina nomi")
    
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    worker_share = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.worker.full_name} - {self.get_work_type_display()} - {self.date}"
    
    def save(self, *args, **kwargs):
        if not self.is_confirmed and self.pk:
            old = WorkDone.objects.get(pk=self.pk)
            if not old.is_confirmed and self.is_confirmed:
                self.worker.current_salary += self.worker_share
                self.worker.save()
                self.confirmed_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_parts_summary(self):
        if self.selected_parts:
            return ", ".join([f"{p['name']}: {p['count']} dona" for p in self.selected_parts])
        return "Ma'lumot yo'q"
    
    class Meta:
        verbose_name = "Bajarilgan ish"
        verbose_name_plural = "Bajarilgan ishlar"
        ordering = ['-date', '-created_at']


class Bonus(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='bonuses')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.worker.full_name} - {self.amount} so'm"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.worker.total_bonuses += self.amount
            self.worker.save()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuslar"


class Payment(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.worker.full_name} - {self.amount} so'm"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.worker.total_paid += self.amount
            self.worker.save()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-payment_date']