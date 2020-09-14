from django.db import models
from django.contrib.auth.models import User
from users.managers import UT
# Create your models here.

CHOICES = (
	('owner','Owner'),
	('tenant','Tenant')
)

# class User(User):

# 	def usertype(self):
# 		usertype = UserType.objects.get(pk=self.id)
# 		return usertype.user_type

class UserType(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ut')
	user_type = models.CharField(max_length=6, choices=CHOICES, default='owner')


	class Meta:
		unique_together = ('user', 'user_type')




class ContactDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_no = models.IntegerField()