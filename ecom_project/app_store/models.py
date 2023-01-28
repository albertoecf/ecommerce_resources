from django.db import models
from django.urls import reverse
from app_category.models import CategoryClass
from app_accounts.models import AccountClass
from django.db.models import Avg


# Create your models here.
class ProductClass(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(CategoryClass, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('app_store:product_detail_path', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRatingClass.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg


variation_category_choice = (
    ('company_stage', 'company_stage'),
    ('company_size', 'company_size'),
)


class VariationManagerClass(models.Manager):
    """
    Custom manager for VariationClass model
    """

    def company_stage(self):
        """
        Returns a queryset of VariationClass objects filtered by variation_category='company_stage' and is_active=True
        """
        return super(VariationManagerClass, self).filter(variation_category='company_stage', is_active=True)

    def company_size(self):
        """
        Returns a queryset of VariationClass objects filtered by variation_category='company_size' and is_active=True
        """
        return super(VariationManagerClass, self).filter(variation_category='company_size', is_active=True)


class VariationClass(models.Model):
    product = models.ForeignKey(ProductClass, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManagerClass()

    def __str__(self):
        return self.variation_category + " : " + self.variation_value


class ReviewRatingClass(models.Model):
    product = models.ForeignKey(ProductClass, on_delete=models.CASCADE)
    user = models.ForeignKey(AccountClass, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
