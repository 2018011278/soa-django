from django.db import models


# Create your models here.
class Qa(models.Model):
    question = models.CharField(max_length=100000)
    answer = models.CharField(max_length=100000)


class pa(models.Model):
    question = models.CharField(max_length=100000)