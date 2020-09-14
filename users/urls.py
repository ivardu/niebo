from django.urls import path, include

from users.views import user_type, settings, account_delete

app_name = 'users'
urlpatterns = [
	path('type/',user_type, name='type'),
	path('acc/',settings, name='settings'),
	path('del/',account_delete, name='del_acc'),
]