from django.shortcuts import render
from django.http import HttpResponse

from .forms import SearchForm
import requests


def test_home(request):
	
	form = SearchForm()

	return render(request, 'renting/home.html', locals())


def renting_house_results(request):
	place = request.POST['place']
	url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'+place+'.json?access_token=pk.eyJ1IjoiaXZhcmR1IiwiYSI6ImNrYm80c2E5NjFnemcycXM0YXE3cTZmaWwifQ.RUzXxKHAH_vuUSs0hc4t7g&limit=1'
	response = requests.get(url)
	json_resp = response.json()
	# print(json_resp, response, json_resp['features'])
	cord = json_resp['features'][0]['center']
	cord = str(cord[0])+','+str(cord[1])
	# print(cord)
	
	return render(request,'renting/renting_house_results.html', locals())

	# return HttpResponse(request.POST['place'])