from django.db import models

class Employee(models.Model):
    DoesNotExist = None
    objects = object
    user_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    # Salary details
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    housing_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def gross_salary(self):
        return self.basic_salary + self.housing_allowance + self.transport_allowance + self.other_allowances

    @property
    def net_salary(self):
        return self.gross_salary - (self.tax_deduction + self.other_deductions)

    def __str__(self):
        return self.name
