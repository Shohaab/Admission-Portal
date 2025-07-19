from django.db import models
from django.contrib.auth.models import User

class Admission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    district = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    picture = models.ImageField(upload_to='students_picture/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
