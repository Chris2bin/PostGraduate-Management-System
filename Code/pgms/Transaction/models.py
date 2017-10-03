from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf','.PNG','.jpg','.gif']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')


class Transaction(models.Model):
    Status = (
        ('Approve', 'Approve'),
        ('Pending', 'Pending'),
    )
    Tran_RefNo = models.CharField(max_length=20)
    Tran_File = models.FileField(upload_to='uploaded_files', validators=[validate_file_extension])
    Date_uploaded = models.DateField(auto_now_add=True, editable=False)
    Tran_Paid = models.DecimalField(max_digits=7, decimal_places=2)
    Tran_Pend = models.CharField(max_length=7, choices=Status, default="Pending")
    StuID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
