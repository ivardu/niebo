from django import forms
from .models import NewRentalHouse, STATE_CHOICES, HouseHas, Amenities, Rules, PreferredTenant, HH_FIELD_CHOICES, FIELD_CHOICES, GENDER_PREF

class SearchForm(forms.Form):
	place = forms.CharField(widget=forms.TextInput(attrs={'class':'input' ,'placeholder':'Search place'}))


class RentalHouseForm(forms.ModelForm):

	house_no = forms.CharField(label='House No',widget=forms.TextInput(attrs={'class':'input', 'placeholder':'House No#'}))
	street_address = forms.CharField(label='Street Address',widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Street Address'}))
	area = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Area'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'City'}))
	state = forms.ChoiceField(label='State/Province', choices=STATE_CHOICES, widget=forms.Select(attrs={'class':'multiple'}))
	zipcode = forms.IntegerField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'ZipCode'}))
	country = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Poland'}), disabled=True, required=False)

	longitude = forms.DecimalField(widget=forms.TextInput(attrs={'class':'input has-background-grey-lighter', 'placeholder':'Longitude'}))
	latitude = forms.DecimalField(widget=forms.TextInput(attrs={'class':'input has-background-grey-lighter', 'placeholder':'Latitude'}))
	
	class Meta:
		model = NewRentalHouse
		fields = '__all__'


		 # widget=forms.TextInput(attrs={'class':'input', 'placeholder':'State'})

# Defining all fields is hectic process

class HouseHasForm(forms.ModelForm):

	bedroom = forms.IntegerField(label='Bedroom', widget=forms.NumberInput(attrs={'class':'input is-small'}))
	kitchen = forms.ChoiceField(choices=HH_FIELD_CHOICES, widget=forms.Select(attrs={'class':'multiple'}))
	bathroom = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	living_room = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	toilet = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	balcony = forms.ChoiceField(choices=HH_FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	terrace = forms.ChoiceField(choices=FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	garden = forms.ChoiceField(choices=FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	basement = forms.ChoiceField(choices=FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	parking = forms.ChoiceField(choices=FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))
	wheelchair_accessible = forms.ChoiceField(choices=FIELD_CHOICES,widget=forms.Select(attrs={'class':'multiple'}))

	class Meta:
		model = HouseHas
		fields = '__all__'
		exclude = ['nrh']

	def __init__(self, *args,**kwargs):
		super().__init__(*args,**kwargs)
		for visible in self.visible_fields():
			visible.field.label_classes=('field-label','is-small')


class AmenitiesForm(forms.ModelForm):

	#This method provides an easy way of definig the choices and widgets for the each field 
	def __init__(self, *args, **kwargs):
		super().__init__()
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'multiple'
			visible.field.choices = FIELD_CHOICES
			# print(visible.field.__dict__)
			visible.field.label_classes = ('field-label','is-small',)
			# print(visible.field.label_classes)

	class Meta:
		model = Amenities
		fields = '__all__'
		exclude = ['nrh']


class RulesForm(forms.ModelForm):

	class Meta:
		model = Rules
		fields = '__all__'
		exclude = ['nrh']

	def __init__(self, *args, **kwargs):
		super().__init__()
		for visible in self.visible_fields():
			# visible.field['gender'].choices = GENDER_PREF
			visible.field.choices = FIELD_CHOICES 


class PreferredTenantForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__()
		for visible in self.visible_fields():
			visible.field.choices = FIELD_CHOICES
		self.fields['gender'].choices = GENDER_PREF

	# gender = forms.ChoiceField(choices=GENDER_PREF)
	
	class Meta:
		model = PreferredTenant
		fields = '__all__'
		exclude = ['nrh']

