from django.urls import path
from renting import views as rt

app_name='renting'
urlpatterns = [
	path('', rt.test_home, name='home'),
	path('disp/', rt.renting_house_results, name='disp')
]