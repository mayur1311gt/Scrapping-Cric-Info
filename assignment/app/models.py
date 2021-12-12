from django.db import models

# Create your models here.
class Player(models.Model):
    player_id=models.AutoField(primary_key=True)
    player_name=models.CharField(max_length=100, blank=True,null=True)
    player_skill=models.CharField(max_length=100,blank=True,null=True)
    player_team=models.CharField(max_length=100, blank=True,null=True)