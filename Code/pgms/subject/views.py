from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from Profile.models import Profile
from django.contrib.auth import logout
from .models import Subject, Enroll
from .forms import EnrollForm

# Create your views here.

def home(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})
    else:
        subjects = Enroll.objects.filter(student = request.user)
        return render(request, 'subject/Subject.html',{'subjects': subjects})

def delete(request, enroll_id):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})

    else:
        enroll = Enroll.objects.get(pk=enroll_id)
        enroll.delete()
        subjects = Enroll.objects.filter(student=request.user)
        return render(request, 'subject/Subject.html',{'subjects':subjects})

def enroll_subject(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})
    else:
        student = request.user
        form = EnrollForm(request.POST or None,initial={'student':student})
        form.fields["subject"].queryset = Subject.objects.exclude(enroll__student = student)
        if form.is_valid():
            enroll = form.save(commit=False)
            enroll.student = request.user
            enroll.save()
            return redirect(reverse('subject:home'))
        context = {
            "form": form
        }
        return render(request, 'subject/enroll.html', context)

