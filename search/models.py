from django.db import models
from django.core.validators import int_list_validator
# Create your models here.


class Document(models.Model):
    title = models.CharField(default='', max_length=100)
    text = models.CharField(default='', max_length=2000)
    subject = models.CharField(default='', max_length=50)
    title_vector = models.CharField(
        max_length=500)
    text_vector = models.CharField(
        max_length=500)
