from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kitchen.views import EmployeeViewSet, VacationDayViewSet, WeeklyPlanViewSet

app_name = 'kitchen'

router = DefaultRouter()
router.register(r'employee', EmployeeViewSet)
router.register(r'vacations', VacationDayViewSet)
router.register(r'weekly-plan', WeeklyPlanViewSet, basename='weekly-plan')


urlpatterns = [
    # path('', include(router.urls)),
]

urlpatterns += router.urls