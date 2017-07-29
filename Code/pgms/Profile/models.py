from django.db import models
from django.conf import settings

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
    ADMIN = 0
    SUPERVISOR = 1
    RESEARCH_STUDENT = 2
    COURSEWORK_STUDENT = 3
    USER_TYPES = (
        (ADMIN, 'Admin'),
        (SUPERVISOR, 'Supervisor'),
        (RESEARCH_STUDENT, 'Research Student'),
        (COURSEWORK_STUDENT, 'Coursework Student'),
    )
    GENDERS = (
        (0, 'Female'),
        (1, 'Male'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    user_dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    user_gender = models.IntegerField(choices=GENDERS, verbose_name="Gender")
    user_address = models.TextField(max_length=500, verbose_name="Address")
    user_photo = models.FileField(default='', verbose_name="Profile Picture")
    user_type = models.IntegerField(choices=USER_TYPES, verbose_name="User Type")

    def __str__(self):
        return "{} - {}".format(self.user, self.USER_TYPES[self.user_type][1] or "")

    class Meta:
        abstract = True

class Students(models.Model):
    # Student status
    STATUS = (
        (0, 'Active'),
        (1, 'Terminated'),
        (2, 'Graduated'),
    )
    # Attributes
    user_status = models.IntegerField(choices=STATUS, verbose_name="Academic Status")
    user_feesOwed = models.FloatField()

    class Meta:
        abstract = True

class ResearchProfile(Students):

    class Meta:
        abstract = True
        verbose_name = 'Student - Research'

    # Progress status
    PROGRESS = (
        (0, 'Thesis Defense'),
        (1, 'Presentation')
    )
    # Attributes
    br_title = models.CharField(max_length=100, verbose_name="Research Title", unique=True)
    br_progress = models.IntegerField(choices=PROGRESS, verbose_name="Research Progress")


class CourseworkProfile(Students):

    class Meta:
        abstract = True
        verbose_name = 'Student - Coursework'

    # Attributes
    bc_cgpa = MinMaxFloat(min_value=0.0, max_value=4.0, verbose_name="CGPA")

class Supervisor(models.Model):
    pass

class Profile(Students, BaseProfile, Supervisor):
    pass

