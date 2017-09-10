from django.db import models
from django.contrib.auth.models import User


# class Supervisor(models.Model):
#     pass
#
# class Student(models.Model):
# #    User_Status = models.CharField(max_length=7, default='studying')
# #    User_FessOwed = models.DecimalField(..., max_digits=5, decimal_places=2, default=00.00)


class Appointment(models.Model):
    Choices = (
        ('Approve', 'Approve'),
        ('Reject', 'Reject'),
        ('Pending', 'Pending'),
    )
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    status = models.CharField(max_length=7, choices=Choices, default='Pending')
    lecID = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='lecID')
    stuID = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stuID')
