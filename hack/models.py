from django.db import models

# Create your models here.

class Profile(models.Model):
    #status 1:activa 0:borrada 2:en confirmacion, active:1:en proceso, active:2:finalizada
    #tags (0 - reasignado , 0 - reagendado)
    _gender = ((1, 'male'), (2, 'female'),)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10)
    company = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=50, null=True)
    gender = models.PositiveSmallIntegerField(choices=_gender,null=True)
    class Meta:
        app_label = 'hack'
        db_table = 'profile'
