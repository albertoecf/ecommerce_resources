from django.db import models
from django.urls import reverse

# Create your models here.
class CategoryClass(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to ='photos/categories',blank=True)


    class Meta:
        verbose_name = "Category Class"
        verbose_name_plural = "Category Class"

    def get_url(self):
        # return sth like  : http://127.0.0.1:8000/store/product-launch
        return reverse('app_store:products_by_category_path',args=[self.slug])

    def __str__(self):
        return self.category_name
