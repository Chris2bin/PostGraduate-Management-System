from .models import Apply, User
from django.shortcuts import render, get_object_or_404
from .forms import ApplyForm, UserForm


def list(request):
	if not request.user.is_authenticated():
		return render(request, 'Application/registration_form.html',{})
	else:
		all_applys = Apply.objects.filter(app_admin=None).exclude(app_admin=request.user)
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
			applys.app_student = user
			applys.app_admin = request.user
			applys.save()
			all_applys = Apply.objects.filter(app_admin=None).exclude(app_admin=request.user)
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
