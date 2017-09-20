from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from Profile.models import Profile,Supervise
from django.contrib.auth import logout
from .models import File
from .forms import FileForm

# Create your views here.
def home(request):
    profile = Profile.objects.get(pk=request.user.id)
    if profile.user_type == 'Student':
        s = get_object_or_404(Supervise,s_student = request.user)
        s1 = s.s_supervisor
        s2 = s.s_cosupervisor
        my_files = File.objects.filter(Q(owner=request.user))
        files = File.objects.filter(Q(owner=s1) | Q(owner=s2))
        query = request.GET.get("q")
        if query:
            files = files.filter(
                Q(file_title__contains=query)
            ).distinct()
            my_files = my_files.filter(
                Q(file_title__contains=query)
            ).distinct()
            return render(request, 'file/File.html', {'my_files':my_files,'files': files})
        else:
            return render(request, 'file/File.html', {'my_files':my_files,'files': files})
    if profile.user_type == 'Supervisor':
    
        supervise = Supervise.objects.filter(Q(s_supervisor=request.user) | Q(s_cosupervisor=request.user))
        for s in supervise:
            files = File.objects.filter(Q(owner=s.s_student))
        my_files = File.objects.filter(Q(owner=request.user))
        query = request.GET.get("q")
        if query:
            files = files.filter(
                Q(file_title__contains=query) 
            ).distinct()
            my_files = my_files.filter(
                Q(file_title__contains=query)
            ).distinct()

            return render(request, 'file/File.html', {'my_files':my_files,'files': files})
        else:
            return render(request, 'file/File.html', {'my_files':my_files,'files': files})
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
                return redirect(reverse('file:home'))

        else:
            form = FileForm()
        return render(request, 'file/upload.html', {'form': form})

def delete_file(request, file_id):
        file = File.objects.get(pk=file_id)
        file.delete()
        profile = Profile.objects.get(pk=request.user.id)
        if profile.user_type == 'Student':
            s = get_object_or_404(Supervise, s_student=request.user)
            s1 = s.s_supervisor
            s2 = s.s_cosupervisor
            my_files = File.objects.filter(Q(owner=request.user))
            files = File.objects.filter(Q(owner=s1) | Q(owner=s2))
            query = request.GET.get("q")
            if query:
                files = files.filter(
                    Q(file_title__contains=query)
                ).distinct()
                my_files = my_files.filter(
                    Q(file_title__contains=query)
                ).distinct()
                return render(request, 'file/File.html', {'my_files': my_files, 'files': files})
            else:
                return render(request, 'file/File.html', {'my_files': my_files, 'files': files})
        if profile.user_type == 'Supervisor':
            files = []
            my_files = []
            supervise = Supervise.objects.filter(Q(s_supervisor=request.user) | Q(s_cosupervisor=request.user))
            for s in supervise:
                file = File.objects.filter(Q(owner=s.s_student))
                for i in file:
                    files.append(i)
            file = File.objects.filter(owner=request.user)
            for j in file:
                my_files.append(j)

            query = request.GET.getlist('files')
            if query:
                for s in files:
                    files = s.Filter(
                        Q(file_title__contains__in=query)
                    ).distinct()
                return render(request, 'file/File.html', {'my_files': my_files, 'files': files})
            else:
                return render(request, 'file/File.html', {'my_files': my_files, 'files': files})
        else:
            logout(request)
            return render(request, 'Profile/login.html',
                          {'error_message': 'You are NOT allowed to enter this page.'})