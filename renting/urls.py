from django.urls import path
from renting import views as rt

app_name='renting'
urlpatterns = [
	path('', rt.test_home, name='home'),
	path('disp/', rt.renting_house_results, name='disp'),
	path('post_rent_ad/',rt.rental_post, name='post_rent_ad'),
	# path('save_rent_ad/',rt.save_rent_house, name='save_rent_house'),
]