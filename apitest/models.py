from django.db import models

# Create your models here.

class lodgeunitinfo(models.Model):
    id = models.AutoField(primary_key=True)
    dayprice = models.IntegerField(null=False)
    choice = {
        ('deleted', 'deleted'),
        ('valid', 'valid')
    }
    estate = models.CharField(choices=choice, default='valid', max_length=10, null=False)
    minday = models.IntegerField(null=False)
    maxday = models.IntegerField(null=False)
    tel = models.CharField(max_length=11,null=False)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=500)
    address_id = models.CharField(max_length=50, null=False)
    image_md5 = models.CharField(max_length=100, null=False)

class order(models.Model):
    id = models.AutoField(primary_key=True)
    totalprice = models.IntegerField(default=0,null=False)
    choice = {
        ('done', 'done'),
        ('valid', 'valid'),
        ('cancel', 'cancel'),

    }
    estate = models.CharField(choices=choice, default='valid', max_length=10, null=False)
    guestNum = models.IntegerField(default=1, null=False)
    checkInDate = models.CharField(max_length=20, null=False)
    checkOutDate = models.CharField(max_length=20, null=False)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=500)
    luId = models.IntegerField(null=False)

class others_order(models.Model):
    id = models.AutoField(primary_key=True)
    totalprice = models.IntegerField(default=0, null=False)
    choice = {
        ('yes', 'yes'),
        ('no', 'no')
    }
    estate = models.CharField(choices=choice, default='no',max_length=10, null=False)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=500)
    order_id = models.IntegerField(null=False)

