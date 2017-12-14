from django.db import models

class UserInfo(models.Model) :
    name = models.CharField(max_length=32)
    sex = models.CharField(max_length=32)
class Role(models.Model) :
    name = models.CharField(max_length=32)

