from django.db import models
from django.urls import reverse


class List(models.Model):
    
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Movie(models.Model):
    title = models.TextField(default='')
    movielist = models.ForeignKey(List, default=None, on_delete=models.CASCADE,)

