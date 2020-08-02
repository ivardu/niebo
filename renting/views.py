from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import SearchForm, RentalHouseForm, HouseHasForm, AmenitiesForm, RulesForm, PreferredTenantForm
from .models import NewRentalHouse, HouseHas, Amenities, PreferredTenant, Rules
import requests, pgeocode, pandas, json

# url = reverse_lazy('renting:house_amenities')

def test_home(request):
	
	form = SearchForm()

	return render(request, 'renting/home.html', locals())


def renting_house_results(request):
	PUB_KEY = settings.MAPBOX_PUBLIC_KEY
	if request.method == 'POST':
		place = (request.POST['place']).replace('#','')
		url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'+place+'.json?access_token=pk.eyJ1IjoiaXZhcmR1IiwiYSI6ImNrYm80c2E5NjFnemcycXM0YXE3cTZmaWwifQ.RUzXxKHAH_vuUSs0hc4t7g&limit=1'
		response = requests.get(url)
		json_resp = response.json()
		cord = json_resp['features'][0]['center']
		cord = str(cord[0])+','+str(cord[1])
		request.session['cord'] = cord
		place_name = (json_resp['features'][0]['place_name']).split(',')[0]

		house_list = NewRentalHouse.objects.filter(city=place_name)
		features = []
		houses_list = []
				

		if house_list:
			# print('satisfied')
			for hous_obj in house_list:

				item = {
				      "type": "Feature",
				      "geometry": {
				        "type": "Point",
				        "coordinates": [
				          hous_obj.longitude,
				          hous_obj.latitude
				        ]
				      },
				      "properties": {
				      	'house_no':hous_obj.house_no,
				        "street_address":hous_obj.street_address,
				        "postalCode": hous_obj.zipcode,
				        "city": hous_obj.city,
				        "country": hous_obj.country,
				      }
				    }
				house = {
					'house_no':hous_obj.house_no,
					'street_address':hous_obj.street_address,
					'zipcode':hous_obj.zipcode,
					'city':hous_obj.city,
					'country':hous_obj.country
				}

				features.append(item)
				houses_list.append(house)

			house = {
				"type": "FeatureCollection",
				"features":features
	  		}
			house = json.dumps(house, cls=DjangoJSONEncoder)

		else:
			# print('Else is executing')
			house = {
				"type": "FeatureCollection",
				"features":None
	  		}
			house = json.dumps(house, cls=DjangoJSONEncoder)
			
			# return HttpResponseRedirect(reverse('renting:disp'))
			return render(request, 'renting/renting_house_results.html', locals())


	else:
		cord = request.session.get('cord', '21.01,52.22')

	
	return render(request,'renting/renting_house_results.html', locals())

	# return HttpResponse(request.POST['place'])


# Make it as only post
@login_required
def post_rent_ad(request):
	form = RentalHouseForm(initial={'country':'Poland'}, data=request.POST or None)
	PUB_KEY = settings.MAPBOX_PUBLIC_KEY
	if request.method == 'POST':
		if form.is_valid():
			rh_obj = form.save()
			data = {'url':reverse_lazy('renting:house_amenities'),
				'id': rh_obj.id}

			return JsonResponse(data)

######### You Need to Handle the Form Errors Too ########### 

		else:
			form_errors = form.errors.items()
			print(form_errors)
			data = dict()
			if form_errors:
				for field,value in form_errors:
					# print(field)
					if field == 'house_no':
						data.update({field:value[0]})
					else:
						data.update({field:value[0]})
			# data.update({"success":False})
			# print(data)
			return JsonResponse(data, status=409)

	else:
		return render(request, 'renting/rental_post.html', locals())
@login_required
def update_rent_ad(request, id):

	try:
		rh_obj = NewRentalHouse.objects.get(pk=id)
		form = RentalHouseForm(data=request.POST or None, instance=rh_obj)
	except:
		rh_obj = None

	if request.method == 'POST' and rh_obj:
		if form.is_valid():
			rh_obj = form.save()
			data = {'url':reverse_lazy('renting:house_amenities'),
				'id': rh_obj.id}

			return JsonResponse(data)

######### You Need to Handle the Form Errors Too ########### 

		else:
			# print(form.errors)
			# print('errors')
			data = {
			 'error':'check djangoconsole'
			}
			return JsonResponse(data, status=404)

	else:

		return HttpResponse('object not found')


	


# To get the HTML code of the House and Amenities
def get_ha_code(request):
	hform = HouseHasForm()
	aform = AmenitiesForm()
	return render(request, 'renting/house_has_and_amenities.html', locals())


def get_rp_code(request):
	rform = RulesForm()
	ptform = PreferredTenantForm()

	return render(request, 'renting/rules_and_preferred_tenant.html', locals())


def save_house_has(request, id):
	
	# print(id)
	try:
		nrh_obj = NewRentalHouse.objects.get(pk=id)
		hh_ex_obj = HouseHas.objects.filter(nrh=nrh_obj)
		if hh_ex_obj:
			hh_ex_form = HouseHasForm(data=request.POST or None, instance=hh_ex_obj[0])
			hh_form = None
		else:
			hh_form = HouseHasForm(data=request.POST or None)
		# print(nrh_obj)
	except:
		nrh_obj = None

	if request.method == 'POST' and nrh_obj:
		if hh_form is not None and hh_form.is_valid():
			hh_mod_obj = hh_form.save(commit=False)
			hh_mod_obj.nrh = nrh_obj
			hh_mod_obj.save()

			data = {
				'url':reverse_lazy('renting:house_amenities'),
				'hh_url':reverse_lazy('renting:house_has',args=(nrh_obj.id,))
			}
			# print(data['url'])
			return JsonResponse(data)

		elif hh_ex_form and hh_ex_form.is_valid():
			hh_ex_form.save()

			data = {
				'url':reverse_lazy('renting:house_amenities')
			}
			# print(data['url'])
			return JsonResponse(data)

		else:
			data = {
				'error':hh_form.errors.as_json()
			}
	# 		print(form.errors)
			return JsonResponse(data, status=400)

	else:
		return JsonResponse({
				'error':'Object not found'
			}, status=404)


def save_amenities(request, id):
	try:
		nrh_obj = NewRentalHouse.objects.get(pk=id)
		am_ex_obj = Amenities.objects.filter(nrh=nrh_obj)
		if am_ex_obj:
			a_ex_form = AmenitiesForm(data=request.POST or None, instance=am_ex_obj[0])
			a_form = None
		else:
			a_form = AmenitiesForm(data=request.POST or None)
	except:
		nrh_obj = None

	if request.method == 'POST' and nrh_obj:
		if a_form is not None and a_form.is_valid():
			a_mod_obj = a_form.save(commit=False)
			a_mod_obj.nrh = nrh_obj
			a_mod_obj.save()

			data = {
				'url':reverse_lazy('renting:rules_tenant'),
				'a_url':reverse_lazy('renting:save_amenities',args=(nrh_obj.id,))
			}
			# print(data['url'])
			return JsonResponse(data)

		elif a_ex_form and a_ex_form.is_valid():
			a_ex_form.save() 
			data = {
				'success':'posted'
			}

			return JsonResponse(data)
####### Handle the Json Error message in Jquery, Ajax + django
		else:
			print(a_form.errors)

def save_rules(request, id):
	try:
		nrh_obj = NewRentalHouse.objects.get(pk=id)
		rl_ex_obj = Rules.objects.filter(nrh=nrh_obj)
		if rl_ex_obj:
			r_ex_form = RulesForm(data=request.POST or None, instance=rl_ex_obj[0])
			r_form = None
		else:
			r_form = RulesForm(data=request.POST or None)
	except:
		nrh_obj = None

	if request.method == 'POST' and nrh_obj:
		if r_form is not None and r_form.is_valid():
			r_mod_obj = r_form.save(commit=False)
			r_mod_obj.nrh = nrh_obj
			r_mod_obj.save()

			data = {
				'url':reverse_lazy('renting:rules_tenant'),
				'r_url':reverse_lazy('renting:save_rules',args=(nrh_obj.id,))
			}
			# print(data['url'])
			return JsonResponse(data)
		elif r_ex_form and r_ex_form.is_valid():
			r_ex_form.save()
			data = {
				'success':'posted'
			}

			return JsonResponse(data)
		else:
			print(r_form.errors)


def save_pt(request, id):
	
	try:
		nrh_obj = NewRentalHouse.objects.get(pk=id)
		pt_ex_obj = PreferredTenant.objects.filter(nrh=nrh_obj)
		if pt_ex_obj:
			pt_ex_form = PreferredTenantForm(data=request.POST or None, instance=pt_ex_obj[0])
			pt_form = None
		else:
			pt_form = PreferredTenantForm(data=request.POST or None)
	except:
		nrh_obj = None

	if request.method == 'POST' and nrh_obj:
		if pt_form is not None and pt_form.is_valid():
			pt_mod_obj = pt_form.save(commit=False)
			pt_mod_obj.nrh = nrh_obj
			pt_mod_obj.save()

			data = {
				'url':reverse_lazy('renting:rules_tenant'),
				'e_url':reverse_lazy('renting:edit_whole',args=(nrh_obj.id,)),
				'd_url':reverse_lazy('renting:del_whole',args=(nrh_obj.id,)),
				'h_url':reverse_lazy('renting:home'),
				'pt_url':reverse_lazy('renting:save_pt',args=(nrh_obj.id,))
			}
			return JsonResponse(data)

		elif pt_ex_form and pt_ex_form.is_valid():
			pt_ex_form.save()

			data = {
				'success':'posted'
			}

			return JsonResponse(data)

		else:
			print(pt_form.errors)	

@login_required
def edit_whole(request, id):
	PUB_KEY = settings.MAPBOX_PUBLIC_KEY
	try:
		nrh_obj = NewRentalHouse.objects.get(pk=id)
		hh_fobj = HouseHas.objects.filter(nrh=nrh_obj)
		a_fobj = Amenities.objects.filter(nrh=nrh_obj)
		r_fobj = Rules.objects.filter(nrh=nrh_obj)
		pt_fobj = PreferredTenant.objects.filter(nrh=nrh_obj)

	except:
		nrh_obj = None
		# print(nrh_obj)
	
	if nrh_obj:
		form = RentalHouseForm(instance=nrh_obj)
		if hh_fobj:
			hh_obj = hh_fobj[0]
			hform = HouseHasForm(instance=hh_obj)
		else:
			hform = HouseHasForm()
		if a_fobj:
			a_obj = a_fobj[0]
			aform = AmenitiesForm(instance=a_obj)
		else:
			aform = AmenitiesForm()
		if r_fobj:
			r_obj = r_fobj[0]
			rform = RulesForm(instance=r_obj)
		else:
			rform = RulesForm()
		if pt_fobj:
			pt_obj = pt_fobj[0]
			ptform = PreferredTenantForm(instance=pt_obj)
		else:
			ptform = PreferredTenantForm()

		# return render(request, 'renting/rental_post_edit.html', locals())

	# else:
	# 	return HttpResponse("Page")
		# print(nrh_obj)

	return render(request, 'renting/rental_post_edit.html', locals())

@login_required
def delete_whole(request, id):
	try:
		nrh_obj = NewRentalHouse.objects.get(pk=id)
	except:
		nrh_obj = None

	if nrh_obj:
		nrh_obj.delete()
		return HttpResponseRedirect(reverse('renting:post_rent_ad'))

	else:
		return HttpResponse('Error')



def zipcode_validate(request):
	pl_zip = pgeocode.Nominatim('pl')

	try:
		zip_obj = pl_zip.query_postal_code(request.GET['zipcode'])
		# print(zip_obj, request.GET['zipcode'])
		cond = pandas.isna(zip_obj.community_name)
		# print(zip_obj)
	except:
		zip_obj = None

	if not cond:
		data = {
		'city' : zip_obj.community_name
		}
		# print(zip_obj.community_name)
		return JsonResponse(data)

	else:
		error = {
		 'zipcode':'Enter a valid ZipCode'
		}
		# print(type(error))
		return JsonResponse(error, status=404)

