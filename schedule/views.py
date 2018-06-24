from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .forms import EmployeeForm, JobForm, ShiftForm, AjaxShiftForm
from .models import WorkWeek, Shift, Job
from .chatbot import go_chatbot


@login_required
def dashboard(request):
    week = datetime.now().isocalendar()[1]
    year = datetime.now().year
    return render(request, 'schedule/dashboard.html', {'week': week, 'year': year})


@login_required
def schedule_create_view(request, year=None, week=None):
    work_week, created = WorkWeek.objects.get_or_create(year=year, week=week, workplace=request.user.workplace)
    shifts = work_week.shifts.all() if not created else None
    return render(request, 'schedule/schedule/create.html', {'week': week,
                                                             'year': year,
                                                             'next_week': week+1 if week < 52 else 1,
                                                             'next_year': year if week < 52 else year+1,
                                                             'work_week': work_week,
                                                             'start_datetime': work_week.get_start_datetime(),
                                                             'shifts': shifts})


@login_required
def schedule_finalize(request, year, week):
    work_week = WorkWeek.objects.get(year=year, week=week, workplace=request.user.workplace)
    work_week.finalize_schedule()
    return redirect(work_week.workplace.get_dashboard_url())



@csrf_exempt
def ajax_create_shift(request):
    if request.method == 'POST':
        form = AjaxShiftForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            weekday = cd['work_day']
            workplace = request.user.workplace
            work_week = WorkWeek.objects.get(pk=cd['work_week'])
            job = Job.objects.get(pk=cd['job'])
            start_time = cd['start_time']
            end_time = cd['end_time']
            try:
                new_shift = Shift.objects.create(weekday=weekday,
                                                 workplace=workplace,
                                                 work_week=work_week,
                                                 job=job,
                                                 start_time=start_time,
                                                 end_time=end_time)
                new_shift.save()
            except Exception as E:
                print(E)

            return JsonResponse({'shift_id': new_shift.id,
                                 'job': new_shift.job.name,
                                 'job_slug': new_shift.job.slug,
                                 'start_time': new_shift.start_datetime().isoformat(),
                                 'end_time': new_shift.end_datetime().isoformat(),
                                 'background_color': new_shift.job.color
                                 })
    return JsonResponse({'error': 'sorry'})


@login_required
def employees_view(request):
    employees = request.user.workplace.employee_set.all()
    return render(request, 'schedule/employee/list.html', {'employees':employees})


@login_required
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


@login_required
def jobs_view(request):
    jobs = request.user.workplace.job_set.all()
    return render(request, 'schedule/job/list.html', {'jobs': jobs})


@login_required
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


@login_required
def shifts_view(request):
    shifts = request.user.workplace.shift_set.all()
    return render(request, 'schedule/shift/list.html', {'shifts': shifts})


@login_required
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


@login_required
def dummy_view(request):
    return render(request, 'schedule/schedule/create.html', {})


def txt_me(request):
    if request.method == 'POST':
        params = request.POST
        user_txt = params['Body'] or ''
        user_phone = params['From'] or ''
        print(f'{user_phone} Sent||| {user_txt}')
        go_chatbot(message=user_txt, phone_number=user_phone)

    return HttpResponse('')
