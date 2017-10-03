from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from .models import Profile
from Application.models import Application
from .forms import UserForm, ProfileEditForm, ProgressForm
from Application.forms import ApplicationForm
from Appointment.forms import AppointmentForm
from Appointment.models import Appointment

def login_user(request):
    if request.method == "POST":
        if request.POST.get("login") == "Login":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    profile = Profile.objects.get(pk=request.user.id)
                    try:
                        application = Application.objects.get(app_student=request.user)
                    except Application.DoesNotExist:
                        application = None
                    if profile.user_type == 'Admin':
                        all_applications = Application.objects.filter(app_admin=None).exclude(app_admin=request.user)
                        return render(request,'Application/index.html',{'all_applications':all_applications})
                    else:
                        return redirect('Profile:home')
                else:
                    return render(request, 'Profile/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'Profile/login.html', {'error_message': 'Invalid login'})

        elif request.POST.get("application") == "Application":
            if request.POST:
                form = ApplicationForm(request.POST, request.FILES)
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
                    return render(request, 'Profile/login.html', {'success_message':"Application submit sucessfull!"})
    return render(request, 'Profile/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'Profile/login.html', context)

def home(request):
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
        profile = Profile.objects.get(pk=request.user.id)
        try:
            application = Application.objects.get(app_student=request.user)
        except Application.DoesNotExist:
            application = None
        # Filter away admin profile
        all_profiles = Profile.objects.all().filter(
                Q(user_type="Supervisor") | Q(user_type="Student")
            ).distinct()
        query = request.GET.get("q")
        if query:
            all_profiles = all_profiles.filter(
                Q(user__username__contains=query) | Q(user_type__contains=query) | Q(
                    user__first_name__contains=query) | Q(user__last_name__contains=query)
            ).distinct()
            return render(request, 'Profile/search.html', {'all_profiles': all_profiles, 'profile': profile, 'application': application, })
        else:
            return render(request, 'Profile/home.html', {'profile': profile, 'application': application, })

def search(request):
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
        return render(request, 'Profile/search.html', {'all_profiles': all_profiles, 'profile': profile, })

def profile(request, username):
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
        profile = Profile.objects.get(pk=request.user.id)
        target_profile = Profile.objects.get(user__username=username)
        # Filter away admin profile
        all_profiles = Profile.objects.all().filter(
                Q(user_type="Supervisor") | Q(user_type="Student")
            ).distinct()
        # Search
        query = request.GET.get("q")
        if query:
            all_profiles = all_profiles.filter(
                Q(user__username__contains=query) | Q(user_type__contains=query) | Q(
                    user__first_name__contains=query) | Q(user__last_name__contains=query)
            ).distinct()
            return render(request, 'Profile/search.html', {'all_profiles': all_profiles, 'profile': profile, })

        if profile.user_type == 'Supervisor':
            approved_app = Appointment.objects.filter(lecID=profile.user)
            form = ProgressForm(request.POST or None)
            if request.POST:
                if form.is_valid():
                    progress = form.cleaned_data.get("br_progress")
                    target_profile.br_progress = progress
                    target_profile.save()
            if request.POST.get("reject"):
                appointmentID = request.POST.get('appointment_id', False)
                app = Appointment.objects.get(pk=appointmentID)
                app.status = "Reject"
                app.save()
            elif request.POST.get("accept"):
                appointmentID = request.POST.get('appointment_id', False)
                app = Appointment.objects.get(pk=appointmentID)
                app.status = "Approve"
                app.save()

            return render(request, 'Profile/profile_supervisor.html', {'form': form, 'profile': profile, 'target_profile': target_profile, 'approved_app': approved_app,})
        elif profile.user_type == 'Student':
            try:
                application = Application.objects.get(app_student=request.user.id)
            except Application.DoesNotExist:
                application = None
                approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

            if request.method == "POST":
                if request.POST.get("appointment") == "Appointment":
                    form = AppointmentForm(request.POST or None)
                    if form.is_valid():
                        appointment = form.save(commit=False)
                        appointment.stuID = profile.user
                        appointment.lecID = target_profile.user
                        appointment.save()
                        return render(request, 'Profile/profile_student.html', {'profile': profile, 'target_profile': target_profile, 'application': application, 'approved_app': approved_app,}, {'success_message': "Application submit sucessfull!"})
        return render(request, 'Profile/profile_student.html', {'profile': profile, 'target_profile': target_profile, 'application': application, 'approved_app': approved_app,})


def change_password(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'Profile/home.html', {'profile': profile,})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    profile = Profile.objects.get(pk=request.user.id)
    return render(request, 'Profile/change_password.html', {'form': form, 'profile': profile,})

def edit_profile(request):
    profile_instance, created = Profile.objects.get_or_create(user=request.user)
    profile_edit_form = ProfileEditForm(request.POST or None, instance=profile_instance)
    if request.POST:
        if profile_edit_form.is_valid():
            profile_edit_form.save_all_fields_from_request(request=request)
            profile = Profile.objects.get(pk=request.user.id)
            return render(request, 'Profile/home.html', {'profile': profile,})
    profile = Profile.objects.get(pk=request.user.id)
    return render(request, 'Profile/edit_profile.html', {'form': profile_edit_form, 'profile': profile,})
