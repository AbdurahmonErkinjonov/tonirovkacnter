from django import forms
from django.contrib.auth.models import User
from .models import *

class WorkerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Login", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Parol")
    
    monday_working = forms.BooleanField(required=False, initial=True, label="Dushanba ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    tuesday_working = forms.BooleanField(required=False, initial=True, label="Seshanba ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    wednesday_working = forms.BooleanField(required=False, initial=True, label="Chorshanba ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    thursday_working = forms.BooleanField(required=False, initial=True, label="Payshanba ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    friday_working = forms.BooleanField(required=False, initial=True, label="Juma ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    saturday_working = forms.BooleanField(required=False, initial=True, label="Shanba ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    sunday_working = forms.BooleanField(required=False, initial=True, label="Yakshanba ish kuni", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = Worker
        exclude = ['user', 'current_salary', 'total_fines', 'total_bonuses', 'total_paid']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'late_fine': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'overtime_bonus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'monday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tuesday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tuesday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'wednesday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'wednesday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'thursday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'thursday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'friday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'friday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'saturday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'saturday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sunday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sunday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
        
        
        
    three_hour_bonus_amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False, 
        initial=0,
        label="3 soatdan keyin bonus (so'm)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
)
        
        
        

class WorkerEditForm(forms.ModelForm):
    monday_working = forms.BooleanField(required=False, label="Dushanba", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    tuesday_working = forms.BooleanField(required=False, label="Seshanba", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    wednesday_working = forms.BooleanField(required=False, label="Chorshanba", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    thursday_working = forms.BooleanField(required=False, label="Payshanba", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    friday_working = forms.BooleanField(required=False, label="Juma", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    saturday_working = forms.BooleanField(required=False, label="Shanba", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    sunday_working = forms.BooleanField(required=False, label="Yakshanba", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    three_hour_bonus_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, initial=0,
        label="3 soatdan keyin bonus (so'm)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    class Meta:
        model = Worker
        fields = [
            'full_name', 'salary_percent', 'late_fine', 'overtime_bonus',
            'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end',
            'wednesday_start', 'wednesday_end', 'thursday_start', 'thursday_end',
            'friday_start', 'friday_end', 'saturday_start', 'saturday_end',
            'sunday_start', 'sunday_end',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'late_fine': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'overtime_bonus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'monday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tuesday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tuesday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'wednesday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'wednesday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'thursday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'thursday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'friday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'friday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'saturday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'saturday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sunday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sunday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TonirovkaForm(forms.ModelForm):
    class Meta:
        model = Tonirovka
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tonirovka nomi'}),
        }

class SonsaZashitaForm(forms.ModelForm):
    class Meta:
        model = SonsaZashita
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sonsa zashita nomi'}),
        }

class LaminationFilmForm(forms.ModelForm):
    class Meta:
        model = LaminationFilm
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_meter': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ProtectiveFilmForm(forms.ModelForm):
    class Meta:
        model = ProtectiveFilm
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_meter': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = ['worker', 'amount', 'reason']
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Bonus sababi...'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['worker', 'amount', 'note']
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Izoh...'}),
        }

class SalaryPaidForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), label="Ishchi", widget=forms.Select(attrs={'class': 'form-control'}))

from django import forms
from .models import *

class TonirovkaWorkForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        label="Ishchi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tonirovka = forms.ModelChoiceField(
        queryset=Tonirovka.objects.all(),
        label="Tonirovka turi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    car_name = forms.CharField(
        max_length=255,
        label="Mashina nomi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina nomi...'})
    )
    rear_door = forms.IntegerField(
        min_value=0, initial=0,
        label="Orqa eshik oynasi (uvol)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    front_door = forms.IntegerField(
        min_value=0, initial=0,
        label="Oldi eshik oynasi (uvol)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rear_windshield = forms.IntegerField(
        min_value=0, initial=0,
        label="Orqa lobovoy",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    front_windshield = forms.IntegerField(
        min_value=0, initial=0,
        label="Oldi lobovoy",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class SonsaWorkForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        label="Ishchi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sonsa = forms.ModelChoiceField(
        queryset=SonsaZashita.objects.all(),
        label="Sonsa zashita turi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    car_name = forms.CharField(
        max_length=255,
        label="Mashina nomi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina nomi...'})
    )
    rear_door = forms.IntegerField(
        min_value=0, initial=0,
        label="Orqa eshik oynasi (uvol)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    front_door = forms.IntegerField(
        min_value=0, initial=0,
        label="Oldi eshik oynasi (uvol)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rear_windshield = forms.IntegerField(
        min_value=0, initial=0,
        label="Orqa lobovoy",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    front_windshield = forms.IntegerField(
        min_value=0, initial=0,
        label="Oldi lobovoy",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class LaminationWorkForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        label="Ishchi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    lamination_film = forms.ModelChoiceField(
        queryset=LaminationFilm.objects.all(),
        label="Laminatsiya plyonkasi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    car_name = forms.CharField(
        max_length=255,
        label="Mashina nomi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina nomi...'})
    )
    is_detailed = forms.ChoiceField(
        choices=[('true', 'Yechilgan detallar'), ('false', 'Yechilmagan detallar')],
        label="Detallar holati",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    meters_used = forms.DecimalField(
        max_digits=10, decimal_places=2,
        label="Ketgan metr",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

class BronWorkForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        label="Ishchi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    protective_film = forms.ModelChoiceField(
        queryset=ProtectiveFilm.objects.all(),
        label="Bron plyonka",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    car_name = forms.CharField(
        max_length=255,
        label="Mashina nomi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina nomi...'})
    )
    meters_used = forms.DecimalField(
        max_digits=10, decimal_places=2,
        label="Ketgan metr",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    
    

class CarForm(forms.ModelForm):
    """Mashina qo'shish formasi"""
    class Meta:
        model = Car
        fields = ['name', 'owner_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina nomi...'}),
            'owner_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
        }


class CarWorkForm(forms.Form):
    """Mashina ishi qo'shish formasi"""
    car = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        label="Mashina",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    work_type = forms.ChoiceField(
        choices=[('tonirovka', 'Tonirovka'), ('sonsa', 'Sonsa Zashita'), 
                 ('laminatsiya', 'Laminatsiya'), ('bron', 'Bron')],
        label="Ish turi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    work_date = forms.DateField(
        required=False,
        label="Ish sanasi",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    total_price = forms.DecimalField(
        max_digits=15, decimal_places=2,
        label="Umumiy narx (so'm)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )   
    
    
    
class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['text', 'image', 'video']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Xabar yozing...'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }