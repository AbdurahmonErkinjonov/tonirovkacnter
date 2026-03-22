from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/workers/', views.workers_list, name='workers_list'),
    path('admin-panel/worker/edit/<int:worker_id>/', views.edit_worker, name='edit_worker'),
    path('admin-panel/worker/delete/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    path('admin-panel/add-worker/', views.add_worker, name='add_worker'),
    path('admin-panel/add-holiday/', views.add_holiday, name='add_holiday'),
    path('admin-panel/add-tonirovka/', views.add_tonirovka, name='add_tonirovka'),
    path('admin-panel/add-sonsa/', views.add_sonsa, name='add_sonsa'),
    path('admin-panel/add-laminatsiya/', views.add_laminatsiya, name='add_laminatsiya'),
    path('admin-panel/add-bron/', views.add_bron, name='add_bron'),
    path('admin-panel/add-bonus/', views.add_bonus, name='add_bonus'),
    path('admin-panel/salary-paid/', views.salary_paid, name='salary_paid'),
    path('admin-panel/payment/', views.payment, name='payment'),
    path('admin-panel/reports/', views.reports, name='reports'),
    
    
    # Worker panel
    path('worker-panel/', views.worker_dashboard, name='worker_dashboard'),
    path('worker-panel/check-in/', views.check_in, name='check_in'),
    path('worker-panel/check-out/', views.check_out, name='check_out'),
    path('worker-panel/work-done/', views.work_done, name='work_done'),
    path('worker-panel/tonirovka-work/', views.tonirovka_work, name='tonirovka_work'),
    path('worker-panel/sonsa-work/', views.sonsa_work, name='sonsa_work'),
    path('worker-panel/laminatsiya-work/', views.laminatsiya_work, name='laminatsiya_work'),
    path('worker-panel/bron-work/', views.bron_work, name='bron_work'),
]