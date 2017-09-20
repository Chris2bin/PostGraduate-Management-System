from django.db import models
from django.conf import settings
import datetime
from Profile.models import BaseProfile
# Create your models here.

class File(models.Model):
    file_title = models.CharField(max_length=250, blank=False)
    file_upload = models.FileField(upload_to='File/')
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='file', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.file_title + ' ( ' + self.owner.username + ')'


