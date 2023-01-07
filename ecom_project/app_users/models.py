from django.db import models

# Create your models here.
class UserClass(models.Model):

    user_id = models.IntegerField()
    photo = models.ImageField(upload_to = 'photos/%Y/%m/%d')
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length =100)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'User Class'
        verbose_name_plural = 'User Class'

    def __str__(self):
        return self.name
