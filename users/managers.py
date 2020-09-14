from django.db import models 


class UT(models.Manager):

	def get_queryset(self):
		print(self.get_queryset())
		print(super().get_queryset())
		return super().get_queryset().user_type
 