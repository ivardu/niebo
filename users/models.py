from django.db import models
from django.contrib.auth.models import User
# Create your models here.

CHOICES = (
	('owner','Owner'),
	('tenant','Tenant')
)

class UserType(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	user_type = models.CharField(max_length=6, choices=CHOICES, default='owner')


class ContactDetails(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	phone_no = models.IntegerField()