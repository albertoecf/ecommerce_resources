from django.db import models

# Create your models here.
class CategoryClass(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to ='photos/categories',blank=True)


    class Meta:
        verbose_name = "Category Class"
        verbose_name_plural = "Category Class"


    def __str__(self):
        return self.category_name
