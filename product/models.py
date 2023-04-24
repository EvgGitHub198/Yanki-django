from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    category_image = models.ImageField(upload_to='uploads/category_images/', blank=True, null=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'


class Size(models.Model):
   XS = 'XS'
   S = 'S'
   M = 'M'
   L = 'L'
   XL = 'XL'
   XXL = 'XXL'

   CHOICES = (
       (XS, 'Extra Small'),
       (S, 'Small'),
       (M, 'Medium'),
       (L, 'Large'),
       (XL, 'Extra Large'),
       (XXL, 'Double Extra Large'),
   )
   name = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
   


   def __str__(self):
       return self.name


class Product(models.Model):
   category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
   name = models.CharField(max_length=200)
   slug = models.SlugField(unique=True)
   description = models.TextField(blank=True, null=True)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   main_image = models.ImageField(upload_to='uploads/main_images', blank=True, null=True)
   extra_images = models.ManyToManyField('ExtraImage', related_name='products', blank=True)
   sizes = models.ManyToManyField(Size, through='ProductSize', blank=True)
   date_added = models.DateTimeField(auto_now_add=True)

   class Meta:
       ordering = ('-date_added',)

   def __str__(self):
       return self.name

   def get_absolute_url(self):
       return f'/{self.category.slug}/{self.slug}'

class ExtraImage(models.Model):
    image = models.ImageField(upload_to='uploads/extra_images', blank=True, null=True)

    def __str__(self):
        return self.image.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='size_quantities', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')


    def __str__(self):
        return f'{self.product}'

