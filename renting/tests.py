from django.test import TestCase

# Create your tests here.

from .models import NewRentalHouse
from .forms import RentalHouseForm

class HouseAddrTest(TestCase):

	def setUp(self):
		self.form = RentalHouseForm(data={'csrfmiddlewaretoken': 'al5JJ7DcROZVfMkUsV045WlUOLmjmjCg5AaOUMJgaHCWFrr1phBMhHn2arEughNi', 'street_address': 'Testing', 'area': 'New Hasnabad', 'city': 'Testing', 'state': 'Lower Silesia', 'zipcode': '560033', 'longitude': '20.98', 'latitude': '52.23'})
		# self.form.is_valid()
		# print(self.form.clean())
		# , 'house_no': '456ab'

	def test_house_add_form(self):
		print(self.form.errors.as_json())
		self.assertTrue(self.form.is_valid())



class RentingFormsTest(TestCase):

	def setUp(self):
		# try:
		self.nrh = NewRentalHouse.objects.all()
		# except:
		# 	self.nrh = None

	def test_nrh_form(self):
		# self.assertIs(self.nrh, NewRentalHouse)
		print(self.nrh)



