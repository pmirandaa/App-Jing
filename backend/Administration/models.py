from django.db import models


class Log(models.Model):
    task = models.CharField(max_length=50)
    value_before = models.CharField(max_length=100)
    value_after = models.CharField(max_length=100)
    person = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.task} {self.person}'

