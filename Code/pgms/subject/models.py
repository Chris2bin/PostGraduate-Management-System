from django.db import models
from django.conf import settings
# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=250, blank=False)
    credit_hour = models.IntegerField(blank = False)
    fee = models.DecimalField(max_digits=7,decimal_places=2,blank = False)
    def __str__(self):
        return self.name



class Enroll(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default="0.00")

    def __str__(self):
        return self.student.username + ' - ' + self.subject.name




