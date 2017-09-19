from .models import Apply, User
from django.shortcuts import render, get_object_or_404
from .forms import ApplyForm, UserForm

def ApplyRequire(request):

	if request.POST:
		form = ApplyForm(request.POST,request.FILES)
		app_name_first = request.POST['app_name_first']
		app_name_last = request.POST['app_name_last']
		app_birthday = request.POST['app_birthday']
		app_gender = request.POST['app_gender']
		app_ic = request.POST['app_ic']
		app_nation = request.POST['app_nation']
		app_address = request.POST['app_address']
		app_file_upload = request.FILES['app_file_upload']
		app_file_upload2 = request.FILES['app_file_upload2']
		app_file_upload3 = request.FILES['app_file_upload3']
		app_email = request.POST['app_email']
		app_mobile_number = request.POST['app_mobile_number']
		app_type = request.POST['app_type']
		app_programme = request.POST['app_programme']
		if form.is_valid():
			form.save()
	return render(request, 'Application/registration_form.html', {})


def list(request):
	if not request.user.is_authenticated():
		return render(request, 'Application/registration_form.html',{})
	else:
		all_applys = Apply.objects.filter(user=request.user)
		return render(request,'Application/index.html',{'all_applys':all_applys})

def detail(request, apply_id):
	if not request.user.is_authenticated():
		return render(request, 'Application/registration_form.html',{})
	else:
		applys = get_object_or_404(Apply, pk=apply_id)
		form = UserForm(request.POST or None)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = User(email=applys.app_email,username=username,password=password,first_name=applys.app_name_first,last_name=applys.app_name_last)
			user.save()
			profile = Profile(user=user, user_address=applys.app_address, user_dob=applys.app_birthday, user_photo=applys.app_file_upload2,user_gender=applys.app_gender,stud_type=applys.app_type)
			profile.save()
			applys.delete()
			all_applys = Apply.objects.all()
			return render(request,'Application/index.html',{'all_applys':all_applys})
		context= {
			"applys" : applys,
			"form" : form,
		}
		return render(request, 'Application/detail.html', context)

def delete_apply(request, apply_id):
	if not request.user.is_authenticated():
		return render(request, 'Application/registration_form.html',{})
	else:
		applys = get_object_or_404(Apply, pk=apply_id)
		applys.delete()
		all_applys = Apply.objects.all()
		return render(request, 'Application/index.html', {'all_applys':all_applys})