import random
from datetime import date, datetime, timedelta
from random import choice

from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import KitchenServicePlan, Employee, VacationDay
from .serializer import EmployeeSerializer, VacationDaySerializer, KitchenServicePlanSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {'Employee': serializer.data}
        return Response(response, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = {'Employee': serializer.data}
        return Response(response)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {'Employee': serializer.data}
        return Response(response)


class VacationDayViewSet(viewsets.ModelViewSet):
    queryset = VacationDay.objects.all()
    serializer_class = VacationDaySerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {'Vacations Days': serializer.data}
        return Response(response, headers=headers)

    def list(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        response = {'data': serializer.data}
        return Response({"Vacations Days": response['data']})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {'data': serializer.data}
        return Response({"Vacations Days": response['data']})


class WeeklyPlanViewSet(viewsets.ModelViewSet):
    queryset = KitchenServicePlan.objects.all()
    serializer_class = KitchenServicePlanSerializer

    @action(detail=False, methods=['get'])
    def working_days(self, request):
        date_str = self.request.query_params.get('date', None)
        if date_str:
            working_days = self.get_working_days(date_str)
            return Response(working_days)
        else:
            return Response(status=400, data={'message': 'Please provide a valid date.'})

    def get_working_days(self, date_str):
        # Convert the input date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Define the order of days of the week
        days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        # Calculate the index of the given day
        day_index = date.weekday()

        # Calculate the number of days before and after the given day
        days_before = day_index
        days_after = len(days_order) - day_index - 1

        # Calculate the start and end dates for the working days
        start_date = date - timedelta(days=days_before)
        end_date = date + timedelta(days=days_after)

        # Generate the employee schedule for the given dates
        schedule = self.generate_employee_schedule(start_date, end_date)

        # Initialize the weekly plan list
        weekly_plan = []

        # Generate a list of working days with employee availability
        for day in range((end_date - start_date).days + 1):
            current_day = start_date + timedelta(days=day)
            if current_day.weekday() < 5:  # 0-4 represents Monday to Friday
                # Check if there is an employee available for the current day
                employee = schedule.get(current_day.strftime('%Y-%m-%d'))
                if employee:
                    working_day = {
                        'date': current_day.strftime("%Y-%m-%d"),
                        'day_of_week': days_order[current_day.weekday()],
                        'employee': employee
                    }
                else:
                    working_day = {
                        'date': current_day.strftime("%Y-%m-%d"),
                        'day_of_week': days_order[current_day.weekday()],
                        'employee': None
                    }
            elif current_day.weekday() == 4:  # Friday
                # Add weekly off for Friday
                working_day = {
                    'date': current_day.strftime("%Y-%m-%d"),
                    'day_of_week': days_order[current_day.weekday()],
                    'employee': 'Weekly Off'
                }
            else:  # Saturday
                # Add weekly off for Saturday
                working_day = {
                    'date': current_day.strftime("%Y-%m-%d"),
                    'day_of_week': days_order[current_day.weekday()],
                    'employee': 'Weekly Off'
                }

            # Append the working day to the weekly plan list
            weekly_plan.append(working_day)

        return {'weekly_plan': weekly_plan}

    def generate_employee_schedule(self, start_date, end_date):
        # Get all employees who are part of the Kitchen Service Plan
        employees = Employee.objects.filter(is_in_kitchen_plan=True)

        # Get the vacation days for all employees
        vacation_days = VacationDay.objects.filter(employee__in=employees, start_date__lte=end_date,
                                                   end_date__gte=start_date)

        # Create a list of working days excluding vacation days
        working_days = [day for day in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1))
                        if day.weekday() < 5 and day not in vacation_days]

        # Shuffle the employees list
        shuffled_employees = list(employees)
        random.shuffle(shuffled_employees)

        # Initialize the schedule dictionary
        schedule = {}

        # Track the last assigned day for each employee
        last_assigned_day = {}

        # Assign employees to working days
        for day in working_days:
            if shuffled_employees:
                employee = shuffled_employees.pop()
                # Check if the employee has a vacation on the current day
                if VacationDay.objects.filter(employee=employee, start_date__lte=day, end_date__gte=day).exists():
                    # If the employee has a vacation, get another available employee
                    available_employees = shuffled_employees + [employee]
                    employee = next(emp for emp in available_employees if
                                    not VacationDay.objects.filter(employee=emp, start_date__lte=day,
                                                                   end_date__gte=day).exists())
                    shuffled_employees.remove(employee)

                # Check if the employee was assigned on the last assigned day
                if employee in last_assigned_day and last_assigned_day[employee] == day - timedelta(days=7):
                    # If the employee was assigned on the last assigned day, get another available employee
                    available_employees = shuffled_employees + [employee]
                    employee = next(emp for emp in available_employees if
                                    (emp not in last_assigned_day or last_assigned_day[emp] != day))

                # Update the last assigned day for the employee
                last_assigned_day[employee] = day

                schedule[day.strftime('%Y-%m-%d')] = employee.name
            else:
                schedule[day.strftime('%Y-%m-%d')] = None

        return schedule

    def list(self, request, *args, **kwargs):
        date_str = self.request.query_params.get('date', None)
        if date_str:
            # Convert the date string from the request to a datetime object
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Calculate the start and end dates of the desired week
            start_date = date - timedelta(days=date.weekday())
            end_date = start_date + timedelta(days=4)  # Assuming 5 working days in a week

            # Generate the employee schedule for the week
            schedule = self.generate_employee_schedule(start_date, end_date)

            # Prepare the weekly plan list
            weekly_plan = []
            for day in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
                if day.weekday() < 5:  # 0-4 represents Monday to Friday (working days)
                    employee = schedule.get(day.strftime('%Y-%m-%d'))
                    working_day = {
                        'date': day.strftime("%Y-%m-%d"),
                        'employee': employee
                    }
                    weekly_plan.append(working_day)

            return Response({'weekly_plan': weekly_plan})

        else:
            return Response(status=400, data={'message': 'Please provide a valid date.'})
