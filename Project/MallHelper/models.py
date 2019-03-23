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
		
class places (models.Model):
    placeid = models.AutoField(primary_key=True)
    x = models.FloatField()
    y = models.FloatField()
    name = models.CharField(max_length=255)
    mapid = models.ForeignKey('maps', on_delete=models.CASCADE, db_column='mapid')
    class Meta:
        db_table = "places"


class recomendations (models.Model):
    recomendationid = models.AutoField(primary_key=True)
    message = models.CharField(max_length=255)
    placeid = models.ForeignKey('places', on_delete=models.CASCADE, db_column='placeid')
    class Meta:
        db_table = "recomendations"


class attributes (models.Model):
    attributeid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    value = models.TextField()
    class Meta:
        db_table = "attributes"


class recomendationsattributes (models.Model):
    id = models.AutoField(primary_key=True)
    attributeid = models.ForeignKey('attributes', on_delete=models.CASCADE, db_column='attributeid')
    recomendationid = models.ForeignKey('recomendations', on_delete=models.CASCADE, db_column='recomendationid')
    class Meta:
        db_table = "recomendationsattributes"
        unique_together = (('attributeid', 'recomendationid'))