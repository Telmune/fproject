import random
import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def rand_slug():
    """
    Generate a random slug of length 3 composed of lowercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
class Category(models.Model):
    """
     Class representing a category with name, parent, slug, and creation date.
     """
    name = models.CharField('Категория',max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
    )
    slug = models.SlugField('URL',max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Дата создания',auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save the object to the database.
        """

        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' +self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category-list', args=[str(self.slug)])


class Product(models.Model):
    """
       Represents a product in the store.
    """

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField("Название", max_length=250)
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField(
        "Цена", max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField(
        "Изображение", upload_to='images/products/%Y/%m/%d', default='products/products/default.jpg')
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[str(self.slug)])

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)

class ProductProxy(Product):

    object = ProductManager()

    class Meta:
        proxy = True