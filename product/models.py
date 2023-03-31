from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
      
    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'


    

    #   def save(self, *args, **kwargs):
    #     image_resize(self.image, 500, 500)
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)
