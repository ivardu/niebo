from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string

from .forms import SearchForm, RentalHouseForm, HouseHasForm, AmenitiesForm, RulesForm, PreferredTenantForm, HouseImagesForm, HouseImagesEditForm
from .models import NewRentalHouse, HouseHas, Amenities, PreferredTenant, Rules, HouseImages
from users.models import UserType
from users.forms import UserTypeForm

import requests, pgeocode, pandas, json
from datetime import datetime

# url = reverse_lazy('renting:house_amenities')

def home_page(request):
	# User logged in or not
	if request.user.is_authenticated:
		logged = True

		#Getting the logged on user type 
		try:
			ut = request.user.ut.user_type	
		except:
			ut = None	

	form = SearchForm()
	log = 'false'
	return render(request, 'renting/home.html', locals())


def user_signin_status(request):
	if request.user.is_authenticated:
		return JsonResponse({'user':'logged_in'})

	elif request.user.is_anonymous:
		return JsonResponse({'user':'not_logged_in'})


def renting_house_results(request):
	PUB_KEY = settings.MAPBOX_PUBLIC_KEY
	if request.method == 'POST':
		place = (request.POST['place']).replace('#','')
		url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'+place+'.json?access_token=pk.eyJ1IjoiaXZhcmR1IiwiYSI6ImNrYm80c2E5NjFnemcycXM0YXE3cTZmaWwifQ.RUzXxKHAH_vuUSs0hc4t7g&limit=1'
		response = requests.get(url)
		json_resp = response.json()
	
		try:
			place_name = (json_resp['features'][0]['place_name']).split(',')[0]
			cord = json_resp['features'][0]['center']
			cord = str(cord[0])+','+str(cord[1])
			request.session['cord'] = cord

		except:
			place_name = None

		try:
			sort_by = request.POST['sort_by']
			# print(sort_by)
		except:
			sort_by = None

		try:
			bhk = request.POST['bhk']
			# print(sort_by)
		except:
			bhk = 'bhk'
		
		try:
			in_date = request.POST['in_date']
			out_date = request.POST['out_date']
			in_d = datetime.strptime(in_date, '%m/%d/%Y')
			ot_d = datetime.strptime(out_date, '%m/%d/%Y')

		except:	
			in_d = in_date = datetime.today()
			ot_d = out_date = datetime.today()


		if place_name and sort_by:
			if sort_by == 'Ascending':
				house_list = NewRentalHouse.objects.filter(city=place_name, in_date__lte=in_d, out_date__gte=ot_d).order_by('rent')
				# print(house_list)
			elif sort_by == 'Descending':
				# print(sort_by)
				house_list = NewRentalHouse.objects.filter(city=place_name, in_date__lte=in_d, out_date__gte=ot_d).order_by('-rent')				

		elif in_date and out_date and place_name:	
			house_list = NewRentalHouse.objects.filter(city=place_name, in_date__lte=in_d, out_date__gte=ot_d)

		features = []
		houses_list = {}
		bhks = {
			'one':1,'two':2,'three':3,'three_plus':'3+','zero':0
		}
		bhkk = {
			'0BHK':'zero','1BHK':'one','2BHK':'two','3BHK':'three','3+BHK':'three_plus'
		}
				

		if house_list:
			for hous_obj in house_list:
				try:
					rl = Rules.objects.get(nrh=hous_obj)
					pt = PreferredTenant.objects.get(nrh=hous_obj)
					am = Amenities.objects.get(nrh=hous_obj)
					hh = HouseHas.objects.get(nrh=hous_obj)
					proceed = True
				except:
					proceed = False

				if proceed:
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
					      	'id':hous_obj.id,
					      	'house_no':hous_obj.house_no,
					        "street_address":hous_obj.street_address,
					        "postalCode": hous_obj.zipcode,
					        "city": hous_obj.city,
					        "country": hous_obj.country,
							"rent":hous_obj.rent,
					      }
					    }
					bed = hous_obj.househas.bedroom
					if bhk != 'bhk':
						def verify(bed, bhk):
							if bhkk[bhk] == bed:
								houses_list.update({hous_obj:bhk})
								features.append(item)
						verify(bed, bhk)

					else:				
						houses_list.update({hous_obj:str(bhks[bed])+'BHK'})
						features.append(item)


					# features.append(item)
					
					# print(houses_list)
					

			house = {
				"type": "FeatureCollection",
				"features":features
	  		}
			house = json.dumps(house, cls=DjangoJSONEncoder)
			print(house, houses_list)
			# Handling Ajax Post Requests
			if request.is_ajax():
				return render(request, 'renting/house_results_temp.html', locals())


		else:
			# print('Else is executing')
			house = {
				"type": "FeatureCollection",
				"features":None
	  		}
			house = json.dumps(house, cls=DjangoJSONEncoder)
			

	# Handling the Get Request for House Results disp view
	else:
		cord = request.session.get('cord', '21.01,52.22')

	return render(request,'renting/renting_house_results.html', locals())


# Make it as only post
# @login_required
def post_rent_ad(request):
	# print(request.FILES or None)
	form = RentalHouseForm(initial={'country':'Poland'}, data=request.POST or None)
	img_form = HouseImagesForm(files=request.FILES)
	PUB_KEY = settings.MAPBOX_PUBLIC_KEY
	if request.method == 'POST' and request.user.is_authenticated:
		if form.is_valid():
			rh_obj = form.save(commit=False)
			rh_obj.user = request.user
			rh_obj.save()
			if img_form.is_valid():
				for img_file in request.FILES.getlist('images'):
					HouseImages.objects.create(images=img_file, nrh=rh_obj)
			else:
				print(img_form.errors)

			data = {'url':reverse_lazy('renting:house_amenities'),
				'id': rh_obj.id}

			return JsonResponse(data)

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
			return JsonResponse(data, status=409)

	# GET Request
	elif request.user.is_anonymous:
		modl = 'true'
		return render(request, 'renting/rental_post.html', locals())

	# GET Request
	elif request.user.is_authenticated:
		# Saving the User_type
		try:
			ut = UserType.objects.get(user=request.user)
			ut_form = UserTypeForm(data={'user_type':'owner'},instance=ut)
		except:
			ut = None

		if ut:
			if ut_form.is_valid():
				ut_form.save()
		else:
			ut_form = UserTypeForm(data={'user_type':'owner'})
			if ut_form.is_valid():
				ut_obj = ut_form.save(commit=False)
				ut_obj.user = request.user
				ut_obj.save()

		return render(request, 'renting/rental_post.html', locals())



# @login_required
def update_rent_ad(request, id):
	if request.user.is_authenticated:
		try:
			print(request.POST)
			rh_obj = NewRentalHouse.objects.get(pk=id)
			form = RentalHouseForm(data=request.POST or None, instance=rh_obj)
			img_form = HouseImagesEditForm(files=request.FILES)
			print(form, img_form)
		except:
			rh_obj = None

		if request.method == 'POST' and rh_obj:
			if form.is_valid():
				nrh_obj = form.save()
				print(nrh_obj, img_form)
				if img_form.is_valid():
					print(img_form)
					for img_file in request.FILES.getlist('images'):
						HouseImages.objects.create(images=img_file, nrh=nrh_obj)
				else:
					print(img_form.errors)

			else:
				print(form.errors)
				# print('what else', form)
				data = {
				 'error':'check djangoconsole'
				}
				return JsonResponse(data, status=404)

			data = {'url':reverse_lazy('renting:house_amenities'),
				'id': nrh_obj.id}

			return JsonResponse(data)
		else:
			print(rh_obj)

	elif request.user.is_anonymous:
		modl='true'
		return HttpResponseRedirect(reverse('renting:edit_whole', args=(id,)))



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
				'h_url':reverse_lazy('renting:house_details',args=(nrh_obj.id,)),
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

# @login_required
def edit_whole(request, id):
	PUB_KEY = settings.MAPBOX_PUBLIC_KEY
	if request.user.is_authenticated:
		try:
			nrh_obj = NewRentalHouse.objects.get(pk=id)
			hh_fobj = HouseHas.objects.filter(nrh=nrh_obj)
			a_fobj = Amenities.objects.filter(nrh=nrh_obj)
			r_fobj = Rules.objects.filter(nrh=nrh_obj)
			pt_fobj = PreferredTenant.objects.filter(nrh=nrh_obj)
			img_qset = HouseImages.objects.filter(nrh=nrh_obj)

		except:
			nrh_obj = None
			# print(nrh_obj)
		
		if nrh_obj:
			images_list = []
			form = RentalHouseForm(instance=nrh_obj)
			img_form = HouseImagesEditForm()

			if img_qset:
				for img_obj in img_qset:
					images_list.append(img_obj)
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

		return render(request, 'renting/rental_post_edit.html', locals())

	elif request.user.is_anonymous:
		modl = 'true'
		return render(request, 'renting/rental_post_edit.html', locals())

# @login_required
def delete_whole(request, id):
	if request.user.is_authenticated:
		try:
			nrh_obj = NewRentalHouse.objects.get(pk=id)
		except:
			nrh_obj = None

		if nrh_obj:
			nrh_obj.delete()
			return HttpResponseRedirect(reverse('renting:rent_ad_list'))

		# Need to handle the error for exception - object doesn't exists


	elif request.user.is_anonymous:
		modl='true'
		return HttpResponseRedirect(reverse('renting:edit_whole', args=(id,)))



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



def house_details(request, id):
	if request.user.is_authenticated:
		try:
			nrh_obj = NewRentalHouse.objects.get(pk=id)
			r_hh = HouseHas.objects.get(nrh=nrh_obj)
			am = Amenities.objects.get(nrh=nrh_obj)
			pt = PreferredTenant.objects.get(nrh=nrh_obj)
			rl = Rules.objects.get(nrh=nrh_obj)
			imgs = HouseImages.objects.filter(nrh=nrh_obj)
		except:
			nrh_obj = None

		if nrh_obj:
			return render(request, 'renting/house_detail.html', locals())

		######### Handle the error for house object which doesn't exists

	elif request.user.is_anonymous:
		modl='true'
		return render(request, 'renting/house_detail.html', locals())



def rent_ads(request):
	if request.user.is_authenticated:
		house_list = NewRentalHouse.objects.filter(user=request.user)
		houses_list = []
		edit_list = []
		for hous_obj in house_list:
			try:
				rl = Rules.objects.get(nrh=hous_obj)
				pt = PreferredTenant.objects.get(nrh=hous_obj)
				am = Amenities.objects.get(nrh=hous_obj)
				hh = HouseHas.objects.get(nrh=hous_obj)
				proceed = True
			except:
				proceed = False

			if proceed:
				houses_list.append(hous_obj)
			else:
				edit_list.append(hous_obj)


		return render(request, 'renting/ads_list.html', locals())

	elif request.user.is_anonymous:
		modl='true'
		return render(request, 'renting/house_detail.html', locals())


def del_house_image(request,id):
	if request.user.is_authenticated:
		if request.method == 'DELETE':
			try:
				img_obj = HouseImages.objects.get(pk=id)
			except:
				img_obj = None

			if img_obj:
				img_obj.delete()

				return JsonResponse({'object':'deleted'})

			else:
				return JsonResponse({'object':'not_found'},status=404)

