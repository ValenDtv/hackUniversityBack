from django.db import models

# Create your models here.
class users (models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    class Meta:
        db_table = "users"
		
class maps (models.Model):
    mapid = models.AutoField(primary_key=True)
    map = models.TextField()
    level = models.IntegerField()
    name = models.CharField(max_length=255)
    userid = models.ForeignKey('users', on_delete=models.CASCADE, db_column='userid')
    class Meta:
        db_table = "maps"