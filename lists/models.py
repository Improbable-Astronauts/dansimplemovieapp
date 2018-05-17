from django.db import models


class List(models.Model):
    pass


class Movie(models.Model):
    title = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE,)

