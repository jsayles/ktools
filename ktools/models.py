from django.db import models
from django.conf import settings


class TogglClient(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


class TogglProject(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey(TogglClient, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    is_billable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s: %s" % (self.name, self.id)

    class Meta:
        ordering = ['name',]


class TogglEntry(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    project = models.ForeignKey(TogglProject, null=False, on_delete=models.CASCADE)
    start_ts = models.DateTimeField(null=True, blank=True)
    end_ts = models.DateTimeField(null=True, blank=True)
    duration_sec = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
