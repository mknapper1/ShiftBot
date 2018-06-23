from django.db import models

# send help
class Workplace(models.Model):
    Name = models.CharField(max_length=255)
    BossName = models.CharField(max_length=255)

class Shift(models.Model):
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()


class Employee(models.Model):
    Name = models.CharField(max_length=255)
    PhoneNumber = models.CharField(max_length=12)

class Job(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)

