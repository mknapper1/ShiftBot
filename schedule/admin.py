from django.contrib import admin
from .models import Workplace, Job, Shift, Employee, WorkWeek

# Register your models here.
admin.site.register(Workplace)
admin.site.register(Job)
admin.site.register(Shift)
admin.site.register(Employee)
admin.site.register(WorkWeek)
