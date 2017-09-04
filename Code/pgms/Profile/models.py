from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

# Extending FloatField with min_value and max_value
class MinMaxFloat(models.FloatField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(MinMaxFloat, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value' : self.max_value}
        defaults.update(kwargs)
        return super(MinMaxFloat, self).formfield(**defaults)

# Base class
class BaseProfile(models.Model):

    USER_TYPES = (
        ('Admin', 'Admin'),
        ('Supervisor', 'Supervisor'),
        ('Student', 'Student'),
    )
    GENDERS = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    user_dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    user_gender = models.CharField(choices=GENDERS, verbose_name="Gender", max_length=6)
    user_address = models.TextField(max_length=500, verbose_name="Address")
    user_photo = models.FileField(default='', verbose_name="Profile Picture", null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPES, verbose_name="User Type", max_length=10)

    def __str__(self):
        return "{} - {}".format(self.user, self.user_type or "")


    def get_absolute_url(self):
        return reverse('Profile:profile', kwargs={'username': self.user__username})

    class Meta:
        abstract = True


class Students(models.Model):
    # Student type
    STUDENT_TYPE = (
        ('By Research', 'By Research'),
        ('By Coursework', 'By Coursework'),
    )
    # Student status
    STATUS = (
        ('Active', 'Active'),
        ('Terminated', 'Terminated'),
        ('Graduated', 'Graduated'),
    )
    # Progress status
    PROGRESS = (
        ('None', 'None'),
        ('Proposal Defense', 'Proposal Defense'),
        ('Work Completion Seminar', 'Work Completion Seminar'),
        ('Thesis examination', 'Thesis examination'),
        ('Viva voce', 'Viva voce'),
    )
    # Attributes
    user_status = models.CharField(choices=STATUS, verbose_name="Academic Status", blank=True, null=True, max_length=10)
    user_feesOwed = models.FloatField(verbose_name="Outstanding Payment", default=0)
    stud_type = models.CharField(choices=STUDENT_TYPE, verbose_name="Student Type", blank=True, null=True, max_length=13)
    br_title = models.CharField(max_length=100, verbose_name="Research Title", unique=True, null=True, blank=True)
    br_progress = models.CharField(choices=PROGRESS, verbose_name="Research Progress", default='None', max_length=18)
    bc_cgpa = MinMaxFloat(min_value=0.0, max_value=4.0, verbose_name="CGPA", default=0.0)

    class Meta:
        abstract = True


class Supervisor(models.Model):
    class Meta:
        abstract = True

class Profile(BaseProfile, Students, Supervisor):
    pass
