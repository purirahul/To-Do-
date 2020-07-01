from django.db import models
from django.contrib.auth.models import User, auth
# Create your models here.

class List(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    item = models.CharField(max_length = 200)
    completed = models.BooleanField(default = False)

    def __str__(self):
        if self.completed == True :
            return self.item + ' |  Completed '
        else:
            return self.item + ' |  Not Completed '
