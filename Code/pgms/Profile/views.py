from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Profile
from .forms import UserForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.get(pk=request.user.id)
                return redirect('/home/', context_instance=RequestContext(request))
            else:
                return render(request, 'Profile/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Profile/login.html', {'error_message': 'Invalid login'})
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
    profile = Profile.objects.get(user__username=username)
    return render(request, 'Profile/profile.html', {'profile': profile,})