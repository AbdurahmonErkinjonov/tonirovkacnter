from django import template
from django.utils import timezone
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def multiply(value, arg):
    """Ikkita sonni ko'paytirish"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Ikkita sonni bo'lish"""
    try:
        if float(arg) != 0:
            return float(value) / float(arg)
        return 0
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """Ikkita sonni ayirish"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Ikkita sonni qo'shish"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, arg):
    """Foiz hisoblash"""
    try:
        return (float(value) * float(arg)) / 100
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Lug'atdan element olish"""
    return dictionary.get(key)

@register.filter
def range_filter(value):
    """Range yaratish"""
    return range(value)

@register.filter
def split_string(value, separator=','):
    """Stringni bo'lish"""
    return value.split(separator)

@register.filter
def startswith(text, starts):
    """String boshlanishini tekshirish"""
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter
def endswith(text, ends):
    """String tugashini tekshirish"""
    if isinstance(text, str):
        return text.endswith(ends)
    return False

@register.filter
def to_date(value):
    """Timestampni date ga o'girish"""
    try:
        return datetime.fromtimestamp(int(value))
    except (ValueError, TypeError):
        return value

@register.filter
def time_until(value):
    """Vaqtgacha qancha qoldi"""
    try:
        diff = value - timezone.now()
        if diff.days > 0:
            return f"{diff.days} kun"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} soat"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minut"
        else:
            return "hozir"
    except:
        return ""

@register.filter
def time_ago(value):
    """Qancha vaqt oldin"""
    try:
        diff = timezone.now() - value
        if diff.days > 0:
            return f"{diff.days} kun oldin"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} soat oldin"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minut oldin"
        else:
            return "hozirgina"
    except:
        return ""

@register.filter
def currency(value):
    """Pul formatida chiqarish"""
    try:
        return f"{float(value):,.0f} so'm".replace(',', ' ')
    except (ValueError, TypeError):
        return "0 so'm"

@register.filter
def phone_format(value):
    """Telefon raqamini formatlash"""
    if not value:
        return ""
    value = ''.join(filter(str.isdigit, str(value)))
    if len(value) == 9:
        return f"+998 {value[:2]} {value[2:5]}-{value[5:7]}-{value[7:9]}"
    return value

@register.simple_tag
def current_time(format_string='%d.%m.%Y %H:%M'):
    """Hozirgi vaqt"""
    return timezone.now().strftime(format_string)

@register.simple_tag
def query_transform(request, **kwargs):
    """URL ga parametr qo'shish"""
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v
    return updated.urlencode()