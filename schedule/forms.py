from django import forms

from .models import Employee, Job, Shift


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['name', 'job', 'phone_number']


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['name', 'description']


class ShiftForm(forms.ModelForm):

    class Meta:
        model = Shift
        fields = ['name', 'day', 'work_week', 'start_time', 'end_time', 'job']

