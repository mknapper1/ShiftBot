import datetime

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .forms import EmployeeForm, JobForm, ShiftForm
from .models import WorkWeek


def dashboard(request):
    week = datetime.datetime.now().isocalendar()[1]
    year = datetime.datetime.now().year
    return render(request, 'schedule/dashboard.html', {'week': week, 'year': year})


def schedule_create_view(request, year=None, week=None):
    work_week, created = WorkWeek.objects.get_or_create(year=year, week=week, workplace=request.user.workplace)
    shifts = work_week.shifts.all() if not created else None
    return render(request, 'schedule/schedule/create.html', {'week': week,
                                                             'year': year,
                                                             'start_datetime': work_week.get_start_datetime(),
                                                             'shifts': shifts})


def employees_view(request):
    employees = request.user.workplace.employee_set.all()
    return render(request, 'schedule/employee/list.html', {'employees':employees})


def employees_new_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.workplace = request.user.workplace
            new_employee.save()
            return redirect(request.user.workplace.get_employee_list_url())
    else:
        form = EmployeeForm()
    return render(request, 'schedule/employee/create.html', {'form': form})


def jobs_view(request):
    jobs = request.user.workplace.job_set.all()
    return render(request, 'schedule/job/list.html', {'jobs': jobs})


def jobs_new_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.workplace = request.user.workplace
            new_job.save()
            return redirect(request.user.workplace.get_job_list_url())
    else:
        form = JobForm()

    return render(request, 'schedule/job/create.html', {'form': form})


def shifts_view(request):
    shifts = request.user.workplace.shift_set.all()
    return render(request, 'schedule/shift/list.html', {'shifts': shifts})


def shifts_new_view(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            new_shift = form.save(commit=False)
            new_shift.workplace = request.user.workplace
            new_shift.save()
            return redirect(request.user.workplace.get_shift_list_url())
    else:
        form = ShiftForm()

    return render(request, 'schedule/shift/create.html', {'form': form})

def dummy_view(request):
    return render(request, 'schedule/schedule/create.html', {})