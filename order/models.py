from django.db import models

# Create your models here.

class GotOrder(models.Model):
    order_by = models.CharField(max_length=150)
    order_date = models.DateField()
    got_qty = models.IntegerField()
    complete_status = models.BooleanField(default=False)
    # damage_qty = models.IntegerField(default=0)
    # return_qty = models.IntegerField(default=0)
    # distributed_qty = models.IntegerField(default=0)
    # completed_qty = models.IntegerField(default=0)

class Person(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    phone_no = models.CharField(max_length=15)

class DistributedOrder(models.Model):
    got_order = models.ForeignKey(GotOrder,on_delete=models.PROTECT)
    person = models.ForeignKey(Person,on_delete=models.PROTECT)
    distributed_qty = models.IntegerField()
    completed_qty = models.IntegerField(default=0)
    distributed_date = models.DateField()
    damage_qty = models.IntegerField(default=0)
    return_qty = models.IntegerField(default=0)
    complete_status = models.BooleanField(default=False)


