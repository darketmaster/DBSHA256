from django.db import models
from django.utils import timezone

class Release(models.Model):
    name = models.CharField('Name',max_length=30)
    ip = models.CharField("IP",max_length=30)
    port = models.PositiveIntegerField(default=3306)
    database = models.CharField(max_length=30)
    user = models.CharField(max_length=30) 
    password = models.CharField(max_length=30)
    created = models.DateTimeField(editable=False,default=timezone.now)

    def __str__(self):
        return self.name

class SHA256OP(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    ptype = models.CharField(max_length=30)
    value = models.TextField()
    sha256 = models.TextField(default="NA")
    created = models.DateTimeField(editable=False,default=timezone.now)

    def save(self):
        self.save()

    def __str__(self):
        return self.name