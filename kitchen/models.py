import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=255)
    availability_date = models.DateField()
    is_in_kitchen_plan = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.availability_date} - {self.is_in_kitchen_plan}'


@receiver(post_save, sender=Employee)
def create_kitchen_service_plan(sender, instance, created, **kwargs):
    if created:
        KitchenServicePlan.objects.create(date=datetime.date.today(), employee=instance)


class VacationDay(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employee.name} - {self.start_date} - {self.end_date}'


class KitchenServicePlan(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    vacation_days = models.ForeignKey(VacationDay, related_name='service_plans', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.employee.name} - {self.date} - {self.vacation_days}'
