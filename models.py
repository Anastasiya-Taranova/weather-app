import json

from django.db import models as m


class City(m.Model):
    name = m.CharField(max_length=30)

    def __str__(self):
        return self.name
