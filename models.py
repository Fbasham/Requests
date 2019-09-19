from django.db import models


class Supplier(models.Model):
    supplier_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    inventory = models.FloatField()

    def __str__(self):
        return f'{self.supplier_id}'


class Receipt(models.Model):
    supplier_id = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    bol = models.CharField(max_length=20, primary_key=True)
    volume = models.IntegerField()

    def __str__(self):
        return self.bol


    def increment_inventory(self):
        s = Supplier.objects.get(pk=self.supplier_id.supplier_id)
        s.inventory += self.volume
        s.save()


    
