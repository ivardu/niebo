from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from users.forms import UserTypeForm, UserForm
from django.contrib.auth.models import User

# Create your views here.


def user_type(request):

	if request.method == 'POST':
		utform = UserTypeForm(request.POST)
		if utform.is_valid():
			ut_obj = utform.save(commit=False)
			ut_obj.user = request.user
			ut_obj.save()
			print('success')

		return JsonResponse({'data':'success'})


def settings(request):
	usr = request.user
	email = usr.email
	username = usr.username
	form = UserForm(instance=usr)
	return render(request, 'users/settings.html', locals())


def account_delete(request):
	usr_obj = User.objects.get(id=request.user.id)
	usr_obj.delete()

	return HttpResponseRedirect(reverse('renting:home'))