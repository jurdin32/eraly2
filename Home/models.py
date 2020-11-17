from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Usuario(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
