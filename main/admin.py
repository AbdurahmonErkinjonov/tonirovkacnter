from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'salary_percent', 'current_salary', 'total_fines', 'total_bonuses', 'net_salary_display']
    list_filter = ['created_at']
    search_fields = ['full_name', 'user__username']
    readonly_fields = ['current_salary', 'total_fines', 'total_bonuses', 'total_paid', 'created_at']
    
    def net_salary_display(self, obj):
        net = obj.net_salary()
        color = 'green' if net >= 0 else 'red'
        return format_html('<span style="color: {};">{:.0f} so\'m</span>', color, net)
    net_salary_display.short_description = "Sof oylik"
    
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('user', 'full_name', 'salary_percent')
        }),
        ('Jarima va bonuslar', {
            'fields': ('late_fine', 'overtime_bonus')
        }),
        ('Ish vaqti (Dushanba)', {
            'fields': ('monday_start', 'monday_end'),
            'classes': ('collapse',)
        }),
        ('Ish vaqti (Seshanba)', {
            'fields': ('tuesday_start', 'tuesday_end'),
            'classes': ('collapse',)
        }),
        ('Ish vaqti (Chorshanba)', {
            'fields': ('wednesday_start', 'wednesday_end'),
            'classes': ('collapse',)
        }),
        ('Ish vaqti (Payshanba)', {
            'fields': ('thursday_start', 'thursday_end'),
            'classes': ('collapse',)
        }),
        ('Ish vaqti (Juma)', {
            'fields': ('friday_start', 'friday_end'),
            'classes': ('collapse',)
        }),
        ('Ish vaqti (Shanba)', {
            'fields': ('saturday_start', 'saturday_end'),
            'classes': ('collapse',)
        }),
        ('Ish vaqti (Yakshanba)', {
            'fields': ('sunday_start', 'sunday_end'),
            'classes': ('collapse',)
        }),
        ('Hisob-kitob', {
            'fields': ('current_salary', 'total_fines', 'total_bonuses', 'total_paid'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['date', 'name', 'created_at']
    list_filter = ['date']
    search_fields = ['name']
    date_hierarchy = 'date'

@admin.register(Tonirovka)
class TonirovkaAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(SonsaZashita)
class SonsaZashitaAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(LaminationFilm)
class LaminationFilmAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_meter', 'created_at']
    search_fields = ['name']

@admin.register(ProtectiveFilm)
class ProtectiveFilmAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_meter', 'created_at']
    search_fields = ['name']

@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ['worker', 'check_in', 'check_out', 'is_late', 'fine_amount', 'bonus_amount']
    list_filter = ['is_late', 'check_in', 'worker']
    search_fields = ['worker__full_name']
    date_hierarchy = 'check_in'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('worker')

@admin.register(WorkDone)
class WorkDoneAdmin(admin.ModelAdmin):
    list_display = ['worker', 'work_type', 'date', 'total_price', 'worker_share', 'is_confirmed']
    list_filter = ['work_type', 'is_confirmed', 'date', 'worker']
    search_fields = ['worker__full_name', 'car_name']
    date_hierarchy = 'date'
    actions = ['confirm_works']
    
    def confirm_works(self, request, queryset):
        for work in queryset:
            if not work.is_confirmed:
                work.is_confirmed = True
                work.save()
        self.message_user(request, f"{queryset.count()} ta ish tasdiqlandi!")
    confirm_works.short_description = "Tanlangan ishlarni tasdiqlash"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('worker', 'tonirovka', 'sonsa', 'lamination_film', 'protective_film')

@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ['worker', 'amount', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'created_at']
    search_fields = ['worker__full_name', 'reason']
    date_hierarchy = 'created_at'
    actions = ['mark_as_paid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, f"{queryset.count()} ta bonus to'landi deb belgilandi!")
    mark_as_paid.short_description = "To'langan deb belgilash"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['worker', 'amount', 'payment_date', 'created_at']
    list_filter = ['payment_date', 'worker']
    search_fields = ['worker__full_name', 'note']
    date_hierarchy = 'payment_date'