from django.db import models


class Store(models.Model):
    store_number = models.IntegerField(unique=True)
    store_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    store_location = models.CharField(max_length=200)
    county_number = models.IntegerField()
    county = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.store_name


class Product(models.Model):
    item_number = models.IntegerField(unique=True)
    item_desc = models.TextField()
    # name = models.CharField(max_length=200)
    category = models.IntegerField()
    category_name = models.CharField(max_length=200)
    vendor_number = models.IntegerField()
    vendor_name = models.CharField(max_length=200)
    pack = models.IntegerField()
    bottle_volume_ml = models.FloatField()
    state_bottle_cost = models.FloatField()
    state_bottle_retail = models.FloatField()

    def __str__(self):
        return self.item_desc


class Sale(models.Model):
    invoice_number = models.CharField(max_length=200, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    date = models.DateField()
    bottles_sold = models.IntegerField()
    sale_dollars = models.FloatField()
    volume_sold_liters = models.FloatField()
    volume_sold_gallons = models.FloatField()

    def __str__(self):
        return f"Sale of {self.bottles_sold} bottles on {self.date}"
