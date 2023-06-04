from django.contrib import admin

from kitchen.models import Employee, KitchenServicePlan, VacationDay

# Register your models here.

admin.site.register(Employee)
admin.site.register(VacationDay)
admin.site.register(KitchenServicePlan)