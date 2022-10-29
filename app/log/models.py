from datetime import datetime

from django.db import models


class Log(models.Model):
    name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, null=False)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    message = models.TextField(null=True)


class Status(models.Model):
    OK = 0
    ERROR = 1
    STATUS_CHOICES = (
        (OK, 'OK'),
        (ERROR, 'ERROR'),
    )

    name = models.CharField(max_length=255, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OK)
    message = models.TextField(null=True)