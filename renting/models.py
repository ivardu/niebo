from django.db import models

# Create your models here.

STATE_CHOICES = [
	('Lower Silesia','Lower Silesia'),
('Kujawsko_Pomorskie','Kujawsko_Pomorskie'),
('Łódź Province','Łódź Province'),
('Lublin Province','Lublin Province'),
('Lubuskie Province','Lubuskie Province'),
('Małopolska Province','Małopolska Province'),
('Masovia Province','Masovia Province'),
('Masovia Province','Masovia Province'),
('Podkarpackie Province','Podkarpackie Province'),
('Podlasie Province','Podlasie Province'),
('Pomerania Province','Pomerania Province'),
('Silesia Province','Silesia Province'),
('Holy Cross Province','Holy Cross Province'),
('Warmia_Masuria','Warmia_Masuria'),
('Wielkopolska Province','Wielkopolska Province'),
('West Pomerania','West Pomerania')
]

HH_FIELD_CHOICES = (
		('Pr','Private'),
		('Sh','Shared'),
		('No','Not Available'),
	)

FIELD_CHOICES =(
		('Y','Yes'),
		('N','No')
)

GENDER_PREF = (
	('M','MALE'),
	('F','FEMALE'),
	('O','OTHERS')
)

ROOMS = (
	('zero',0),
	('one',1),
	('two',2),
	('three',3),
	('three_plus',4)

)


class NewRentalHouse(models.Model):
	house_no = models.CharField(max_length=100)
	street_address = models.TextField()
	# area = models.CharField(max_length=150)
	city = models.CharField(max_length=150)
	zipcode = models.CharField(max_length=12)
	# state = models.CharField(max_length=100, choices=STATE_CHOICES)
	country = models.CharField(max_length=100, default='Poland')
	
	longitude = models.DecimalField(max_digits=4, decimal_places=2)
	latitude = models.DecimalField(max_digits=4, decimal_places=2)


# class ContactDetails(models.Model):
# 	phone_no = models.IntegerField()

class HouseHas(models.Model):

	bedroom = models.CharField(max_length=11, choices=ROOMS)
	kitchen = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	bathroom = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	living_room = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	toilet = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	balcony = models.CharField(max_length=2, choices=HH_FIELD_CHOICES)
	terrace = models.CharField(max_length=2, choices=FIELD_CHOICES)
	garden = models.CharField(max_length=2, choices=FIELD_CHOICES)
	basement = models.CharField(max_length=2, choices=FIELD_CHOICES)
	parking = models.CharField(max_length=2, choices=FIELD_CHOICES)
	wheelchair_accessible = models.CharField(max_length=2, choices=FIELD_CHOICES)

	nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE) 


class Amenities(models.Model):

	desk = models.CharField(max_length=1, choices=FIELD_CHOICES)
	closet = models.CharField(max_length=1, choices=FIELD_CHOICES)
	tv = models.CharField(max_length=1, choices=FIELD_CHOICES)
	washing_machine = models.CharField(max_length=1, choices=FIELD_CHOICES)
	dryer = models.CharField(max_length=1, choices=FIELD_CHOICES)
	dishwasher = models.CharField(max_length=1, choices=FIELD_CHOICES)
	kitchenware = models.CharField(max_length=1, choices=FIELD_CHOICES)
	wifi = models.CharField(max_length=1, choices=FIELD_CHOICES)
	heating = models.CharField(max_length=1, choices=FIELD_CHOICES)
	air_conditioning = models.CharField(max_length=1, choices=FIELD_CHOICES)
	bed = models.CharField(max_length=1, choices=FIELD_CHOICES)
	furnished = models.CharField(max_length=1, choices=FIELD_CHOICES)

	nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE)


class PreferredTenant(models.Model):
	gender = models.CharField(max_length=1, choices=GENDER_PREF)
	couple_friendly = models.CharField(max_length=1, choices=FIELD_CHOICES)
	bachelor_allowed = models.CharField(max_length=1, choices=FIELD_CHOICES)

	nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE)


class Rules(models.Model):
	animal_allowed = models.CharField(max_length=1, choices=FIELD_CHOICES)
	smoking_allowed = models.CharField(max_length=1, choices=FIELD_CHOICES)
	musical_instrument = models.CharField(max_length=1, choices=FIELD_CHOICES)

	nrh = models.ForeignKey(NewRentalHouse, on_delete=models.CASCADE)





