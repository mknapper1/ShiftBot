from django import forms

from .models import Employee, Job, Shift


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['name', 'job', 'phone_number']


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['name', 'description', 'color']


class ShiftForm(forms.ModelForm):

    class Meta:
        model = Shift
        fields = ['weekday', 'work_week', 'start_time', 'end_time', 'job']


class AjaxShiftForm(forms.Form):
    work_week = forms.IntegerField()
    work_day = forms.IntegerField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    job = forms.IntegerField()
