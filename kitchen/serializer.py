from rest_framework import serializers

from kitchen.models import Employee, VacationDay, KitchenServicePlan


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class VacationDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = VacationDay
        fields = '__all__'


class KitchenServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenServicePlan
        fields = '__all__'
