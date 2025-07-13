from django.db import models

# Create your models here.


class Product(models.Model):
    name= models.CharField(max_length=200)
    price= models.IntegerField()
    description= models.TextField()
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="imgs")
    image = models.ImageField(upload_to='product_images/')

class Other(models.Model):
    title = models.CharField(max_length=20)
    
    price = models.IntegerField(null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="size_or_color")



class Order(models.Model):
    
    Tracking = models.CharField(max_length=100, blank=True, unique=True)
    TypeLivraison = models.CharField(max_length=1,default='0')
    TypeColis = models.CharField(max_length=1,default='0')
    Confrimee = models.CharField(max_length=1, blank=True, default='')
    Client = models.CharField(max_length=100)
    MobileA = models.CharField(max_length=20)
    MobileB = models.CharField(max_length=20, blank=True)
    Adresse = models.CharField(max_length=255)
    IDWilaya = models.CharField(max_length=2)
    Commune = models.CharField(max_length=100,default="",blank=True)
    Total = models.CharField(max_length=20)
    Note = models.TextField(blank=True)
    TProduit = models.CharField(max_length=255)
    Source = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(default=1)
    conferme = models.CharField(max_length=1,default='0')
    datetime = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.Tracking:
            self.Tracking = f"trk-s-{self.id}"
            super().save(update_fields=['Tracking'])

    def __str__(self):
        return f"{self.Client} - {self.Tracking}"


class WilayaInfo(models.Model):
    IDWilaya = models.IntegerField()
    name = models.CharField(max_length=20)
    delivery_home = models.IntegerField(null=True)
    delivery_office = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.name}'
    