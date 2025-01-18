from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'basic_salary', 'net_salary')
