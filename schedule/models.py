from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify


class Workplace(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    boss_name = models.CharField(max_length=255)

    @staticmethod
    def get_employee_list_url():
        return reverse('schedule:employees_view')

    @staticmethod
    def get_job_list_url():
        return reverse('schedule:jobs_view')

    @staticmethod
    def get_shift_list_url():
        return reverse('schedule:shifts_view')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Auto Slugify the title field on save. do not slugify anywhere else!
        """
        self.slug = slugify(self.name)
        super(Workplace, self).save(*args, **kwargs)


class WorkWeek(models.Model):
    week_number = models.IntegerField()
    year = models.IntegerField()
    complete = models.BooleanField(default=False)
    workplace = models.ForeignKey(Workplace, blank=True, null=True, on_delete=models.SET_NULL)


class Job(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Auto Slugify the title field on save. do not slugify anywhere else!
        """
        self.slug = slugify(self.name)
        super(Job, self).save(*args, **kwargs)


class Employee(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL)
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Auto Slugify the title field on save. do not slugify anywhere else!
        """
        self.slug = slugify(self.name)
        super(Employee, self).save(*args, **kwargs)


class Shift(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sunday = 'Sunday'
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    saturday = 'Saturday'
    DAY_CHOICES = (
        (sunday, 'Sunday'),
        (monday, 'Monday'),
        (tuesday, 'Tuesday'),
        (wednesday, 'Wednesday'),
        (thursday, 'Thursday'),
        (friday, 'Friday'),
        (saturday, 'Saturday'),
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES, default=sunday)
    work_week = models.ForeignKey(WorkWeek, null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL)
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    @property
    def filled(self):
        return self.employee is not None







