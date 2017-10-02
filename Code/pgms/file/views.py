from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from Profile.models import Profile,Supervise
from Application.models import Application
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from .models import File
from .forms import FileForm

# Create your views here.

def file(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.user_type == 'Student':
        try:
            s = Supervise.objects.get(s_student = request.user)
            s1 = s.s_supervisor
            s2 = s.s_cosupervisor
            files = File.objects.filter(Q(owner=s1) | Q(owner=s2))
        except ObjectDoesNotExist:
            files = None
        my_files = File.objects.filter(Q(owner=request.user))
        query = request.GET.get("q")
        if query:
            if files != None:
                files = files.filter(
                    Q(file_title__contains=query)
                ).distinct()
            my_files = my_files.filter(
                Q(file_title__contains=query)
            ).distinct()
            return render(request, 'file/File.html', {'my_files':my_files,'files': files,'profile': profile,})
        else:
            return render(request, 'file/File.html', {'my_files':my_files,'files': files,'profile': profile,})

    elif profile.user_type == 'Supervisor':
        files = []
        try:
            supervise = Supervise.objects.filter(Q(s_supervisor=request.user) | Q(s_cosupervisor=request.user))
            for s in supervise:
                files += File.objects.filter(Q(owner=s.s_student))[:]
        except ObjectDoesNotExist:
            files = None
        my_files = File.objects.filter(Q(owner=request.user))
        query = request.GET.get("q")
        if query:
            files = [x for x in files if query in x.file_title]
            my_files = my_files.filter(
                Q(file_title__contains=query)
            ).distinct()

            return render(request, 'file/File.html', {'my_files':my_files,'files': files,'profile': profile,})
        else:
            return render(request, 'file/File.html', {'my_files':my_files,'files': files,'profile': profile,})
    else:
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})


def upload(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})
    else:
        if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.save(commit=False)
                file.owner = request.user
                file.save()
                return redirect(reverse('file:file'))

        else:
            form = FileForm()
        return render(request, 'file/upload.html', {'form': form, 'profile': profile, })


def delete_file(request, file_id):
        file = File.objects.get(pk=file_id)
        file.delete()
        return redirect('file:file')

def peek(request,user):
    profile = Profile.objects.get(pk=user)
    try:
        application = Application.objects.get(app_student=user)
    except Application.DoesNotExist:
        application = None
    return render(request, 'file/peek.html', {'profile': profile, 'application': application })