from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('',
         views.dashboard,
         name='dashboard'),

    path('create/',
         views.schedule_create_view,
         name='schedule_create_view'),

    path('create/<int:year>/<int:week>/',
         views.schedule_create_view,
         name='schedule_create_view'),

    path('finalize/<int:year>/<int:week>/',
         views.schedule_finalize,
         name='schedule_finalize'),


    path('employees/',
         views.employees_view,
         name='employees_view'),

    path('employees/new/',
         views.employees_new_view,
         name='employees_new_view'),

    path('jobs/',
         views.jobs_view,
         name='jobs_view'),

    path('jobs/new/',
         views.jobs_new_view,
         name='jobs_new_view'),

    path('shifts/',
         views.shifts_view,
         name='shifts_view'),

    path('shifts/new/',
         views.shifts_new_view,
         name='shifts_new_view'),

    path('ajax/create/shift/',
         views.ajax_create_shift,
         name='ajax_create_shift'),

    path('txt/me/',
         views.txt_me,
         name='txt_me'),

]
