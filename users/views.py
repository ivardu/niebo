from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from users.forms import UserTypeForm, UserForm, UpdatePhoneNo
from users.models import UserType, ContactDetails

# Create your views here.


def user_type(request):
	if request.user.is_authenticated:
		try:
			ut = UserType.objects.get(user=request.user)
		except:
			ut = None

		if request.method == 'POST' and ut:
			utform = UserTypeForm(data=request.POST, instance=ut)
			if utform.is_valid():
				ut_obj = utform.save()
			else:
				print(ut_form.erros)

			# Handle the form errors

			return JsonResponse({'user_type':ut_obj.user_type.capitalize()})

			
		elif request.method == 'POST':
			utform = UserTypeForm(data=request.POST)
			if utform.is_valid():
				ut_obj = utform.save(commit=False)
				ut_obj.user = request.user
				ut_obj.save()

			# Handle the form errors
			
			return JsonResponse({'user_type':ut_obj.user_type.capitalize()})
			
	else:
		return JsonResponse({'data':'error'},status=404)


def settings(request):
	usr = request.user
	form = UserForm(instance=usr)
	try:
		pno = usr.contactdetails
		# print(pno, usr.contactdetails)
		pform = UpdatePhoneNo(instance=pno)
	except:
		pno = None
		pform = UpdatePhoneNo()

	if request.method == 'POST':
		pform = UpdatePhoneNo(data=request.POST, instance=pno)
		form = UserForm(data=request.POST, instance=usr)
		if pform.is_valid():
			p_obj = pform.save(commit=False)
			p_obj.user = request.user
			p_obj.save()

		if form.is_valid():
			form.save()

		return render(request, 'users/settings.html', locals())
	
	else:
		return render(request, 'users/settings.html', locals())


def account_delete(request):
	usr_obj = User.objects.get(id=request.user.id)
	usr_obj.delete()

	return HttpResponseRedirect(reverse('renting:home'))