from django.db import models

# Create your models here.
class Destination(models.Model):

    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField(default=500)
    offer = models.BooleanField(default=False)

    # class Meta:
    #     app_label = 'dashboard'

class Backgroudpc(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='bacg')

    # class Meta:
    #     app_label = 'dashboard'
