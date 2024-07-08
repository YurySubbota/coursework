from django.db import models


class Equipment(models.Model):
    STATUS_CHOICES = (
        ('ready', 'ready'),
        ('in_rent', 'in_rent'),
        ('booked', 'booked'),
        ('faulty', 'faulty'),
        ('lost', 'lost'),
    )
    CATEGORY_CHOICES = (
        ('mixer', 'mixer'),
        ('turntable', 'turntable'),
        ('headphones', 'headphones'),
        ('amplifier', 'amplifier'),
        ('speaker', 'speaker'),
        ('other', 'other'),
    )
    category = models.CharField(choices=CATEGORY_CHOICES,default='other',max_length=100)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='ready',max_length=100)
    warehouse_place = models.IntegerField(unique=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()


class Photo(models.Model):
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')
