from django.urls import path
from renting import views as rt

app_name='renting'
urlpatterns = [
	path('', rt.home_page, name='home'),
	path('sign/',rt.user_signin_status, name='sgn_status'),
	path('disp/', rt.renting_house_results, name='disp'),
	path('post_ad/', rt.post_rent_ad, name='post_rent_ad'),
	path('update_ad/<int:id>/', rt.update_rent_ad, name='update_rent_ad'),
	path('ha/', rt.get_ha_code, name='house_amenities'),
	path('rp/', rt.get_rp_code, name='rules_tenant'),
	path('hh/<int:id>/', rt.save_house_has, name='house_has'),
	path('sa/<int:id>/', rt.save_amenities, name='save_amenities'),
	path('sr/<int:id>/', rt.save_rules, name='save_rules'),
	path('spt/<int:id>/', rt.save_pt, name='save_pt'),
	path('edw/<int:id>/', rt.edit_whole, name='edit_whole'),
	path('dlw/<int:id>/', rt.delete_whole, name='del_whole'),
	path('zp/', rt.zipcode_validate, name='validate_zip'),
	path('hd/<int:id>/', rt.house_details, name='house_details'),
	path('adlist/', rt.rent_ads, name='rent_ad_list'),
	path('del_img/<int:id>/',rt.del_house_image, name='del_img'),
]