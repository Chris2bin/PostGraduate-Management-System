from .models import Application, User
from django.shortcuts import render, get_object_or_404
from .forms import ApplicationForm, UserForm
from Profile.models import Profile


def list(request):
	if request.user.is_authenticated():
		profile = Profile.objects.get(pk=request.user.id)
		if profile.user_type == 'Admin':
			all_applications = Application.objects.filter(app_admin=None).exclude(app_admin=request.user)
			return render(request,'Application/index.html',{'all_applications':all_applications})
		else:
			return render(request, 'Profile/login.html',{})

def detail(request, application_id):
	if not request.user.is_authenticated():
		return render(request, 'Profile/login.html',{})
	else:
		applications = get_object_or_404(Application, pk=application_id)
		form = UserForm(request.POST or None)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = User(email=applications.app_email,username=username,first_name=applications.app_name_first,last_name=applications.app_name_last)
			user.set_password(password)
			user.save()
			profile = Profile(user=user, user_address=applications.app_address, user_dob=applications.app_birthday, user_photo=applications.app_file_upload2,user_gender=applications.app_gender,stud_type=applications.app_type, user_type="Student")
			profile.save()
			applications.app_student = user
			applications.app_admin = request.user
			applications.save()
			all_applications = Application.objects.filter(app_admin=None).exclude(app_admin=request.user)
			return render(request,'Application/index.html',{'all_applications' : all_applications,'success_message' : "New User created successful"})
		context= {
			"applications" : applications,
			"form" : form,
		}
		return render(request, 'Application/detail.html', context)

def delete_application(request, application_id):
	if request.user.is_authenticated():
		profile = Profile.objects.get(pk=request.user.id)
		if profile.user_type == 'Admin':
			applications = get_object_or_404(Application, pk=application_id)
			applications.delete()
			all_applications = Application.objects.filter(app_admin=None).exclude(app_admin=request.user)
			return render(request, 'Application/index.html',{'all_applications' : all_applications,'reject_message' : "Application has been rejected"})
		else:
			return render(request, 'Profile/login.html',{})
