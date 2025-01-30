from django.db import models

class Person(models.Model):
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    date_time = models.DateTimeField()
    location_id = models.IntegerField()
    id_number = models.CharField(max_length=100, blank=True, null=True)
    verify_code = models.CharField(max_length=100, blank=True, null=True)
    card_no = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
