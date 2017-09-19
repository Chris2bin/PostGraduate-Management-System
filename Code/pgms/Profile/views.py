from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from .models import Profile
from .forms import UserForm, ProfileEditForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(pk=request.user.id)
            if profile.user_status == 'Active':
                if profile.user_type == 'Admin':
                    return redirect('/admin/', context_instance=RequestContext(request))
                else:
                    return redirect('/home/', context_instance=RequestContext(request))
            else:
                return render(request, 'Profile/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Profile/login.html', {'error_message': 'Invalid login'})
    else:
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
        all_profiles = Profile.objects.all()
        query = request.GET.get("q")
        if query:
            all_profiles = all_profiles.filter(
                Q(user__username__contains=query) | Q(user_type__contains=query)
            ).distinct()

            return render(request, 'Profile/home.html', {'all_profiles': all_profiles, 'profile': profile,})
        else:
            return render(request, 'Profile/home.html', {'profile': profile,})

def profile(request, username):
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
        profile = Profile.objects.get(pk=request.user.id)
        target_profile = Profile.objects.get(user__username=username)
        if profile.user_type == 'Supervisor':
            return render(request, 'Profile/profile_supervisor.html', {'profile': profile, 'target_profile': target_profile,})
        elif profile.user_type == 'Student':
            return render(request, 'Profile/profile_student.html', {'profile': profile, 'target_profile': target_profile, })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('Profile:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Profile/change_password.html', {
        'form': form
    })

def edit_profile(request):
    profile_instance, created = Profile.objects.get_or_create(user=request.user)
    profile_edit_form = ProfileEditForm(request.POST or None, instance=profile_instance)
    if request.POST:
        if profile_edit_form.is_valid():
            profile_edit_form.save_all_fields_from_request(request=request)
            return redirect('Profile:home')
    return render(request, 'Profile/edit_profile.html', {'form': profile_edit_form})