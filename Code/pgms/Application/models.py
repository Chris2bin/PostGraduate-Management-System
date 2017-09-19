from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User


class Apply(models.Model):
    GENDER = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )
    TYPE = (
        ('By Research', 'By Research'),
        ('By Coursework', 'By Coursework'),
    )
    PAYMENT = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    )
    app_name_first = models.CharField(max_length=250)
    app_name_last = models.CharField(max_length=250,null=True)
    app_birthday = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    app_gender = models.CharField(choices=GENDER,max_length=6)
    app_ic = models.CharField(max_length=12)
    app_nation = models.CharField(max_length=20,null=True)
    app_address = models.TextField(max_length=100,null=True)
    app_email = models.EmailField(max_length=100)
    app_file_upload = models.FileField(verbose_name="Document",upload_to='File/',null=True)
    app_file_upload2 = models.ImageField(verbose_name="Photo",upload_to='File/',null=True)
    app_mobile_number = models.CharField(max_length=20,null=True)
    app_type = models.CharField(choices=TYPE,max_length=13,null=True)
    app_programme = models.CharField(max_length=100,null=True)
    app_payment_status = models.CharField(choices=PAYMENT,max_length=10,null=True)
    app_file_upload3 = models.FileField(verbose_name="Qualification",upload_to='File/',null=True)
    app_created_at = models.DateTimeField(auto_now_add=True,null=True)
    app_updated_at = models.DateTimeField(auto_now=True,null=True)
    user = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.app_name_first + ' ' + self.app_name_last
