from django.db import models


class Workplace(models.Model):
    name = models.CharField(max_length=255)
    boss_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
    week = models.IntegerField(default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.SET_NULL)
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name




