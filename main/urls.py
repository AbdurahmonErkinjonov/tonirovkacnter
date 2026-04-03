from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Admin panel
    path('admin-panel/get-present-workers/', views.get_present_workers, name='get_present_workers'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/get-workers-data/', views.get_workers_data, name='get_workers_data'),
    path('admin-panel/get-worker-works/<int:worker_id>/', views.get_worker_works, name='get_worker_works'),
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
    path('admin-panel/attendance/', views.attendance_list, name='attendance_list'),
    path('admin-panel/attendance/edit/<int:session_id>/', views.attendance_edit, name='attendance_edit'),
    path('admin-panel/attendance/create/<int:worker_id>/<str:date>/', views.attendance_create, name='attendance_create'),
    path('admin-panel/add-car/', views.add_car, name='add_car'),
    path('admin-panel/cars/', views.cars_list, name='cars_list'),
    path('admin-panel/add-car-work/', views.add_car_work_admin, name='add_car_work_admin'),
    path('admin-panel/pending-works/', views.pending_car_works, name='pending_car_works'),
    path('admin-panel/confirm-work/<int:work_id>/', views.confirm_car_work, name='confirm_car_work'),
    path('admin-panel/work-history/', views.work_history, name='work_history'),path('admin-panel/get-workers-list/', views.get_workers_list, name='get_workers_list'),
    path('admin-panel/get-worker-details/<int:worker_id>/', views.get_worker_details, name='get_worker_details'),
    path('admin-panel/get-worker-monthly-data/<int:worker_id>/', views.get_worker_monthly_data, name='get_worker_monthly_data'),
    # Worker panel
    path('worker-panel/', views.worker_dashboard, name='worker_dashboard'),
    path('worker-panel/check-in/', views.check_in, name='check_in'),
    path('worker-panel/check-out/', views.check_out, name='check_out'),
    path('worker-panel/work-done/', views.work_done, name='work_done'),
    path('worker-panel/add-car-work/<int:car_id>/', views.worker_add_car_work, name='worker_add_car_work'),
    
    # API
    path('api/car-parts/', views.api_car_parts, name='api_car_parts'),
    
    
    #chat
    path('messenger/', views.messenger, name='messenger'),
    path('messenger/delete/<int:message_id>/', views.messenger_delete_message, name='messenger_delete_message'),
    path('admin-panel/discipline-ranking/', views.discipline_ranking, name='discipline_ranking'),
    path('admin-panel/reset-discipline-stats/', views.reset_discipline_stats, name='reset_discipline_stats'),
    path('worker-panel/discipline-ranking/', views.worker_discipline_ranking, name='worker_discipline_ranking'),
]