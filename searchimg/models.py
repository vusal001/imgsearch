from django.db import models

# Create your models here.



class sekil(models.Model):
    image = models.ImageField(upload_to='uploaded/')


