from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Users(models.Model):
    # user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
