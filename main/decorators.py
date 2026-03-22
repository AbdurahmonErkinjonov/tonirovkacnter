from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Bu sahifaga faqat adminlar kirishi mumkin!")
            return redirect('worker_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def worker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_staff:
            messages.error(request, "Bu sahifaga faqat ishchilar kirishi mumkin!")
            return redirect('admin_dashboard')
        if not hasattr(request.user, 'worker'):
            messages.error(request, "Siz ishchi emassiz!")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper