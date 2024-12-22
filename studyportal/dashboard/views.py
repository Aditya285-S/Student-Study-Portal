from django.shortcuts import render, redirect
from .models import Notes
from django.contrib import messages
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')



@login_required
def notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            notes = Notes(user = request.user, title = title, description = description)
            notes.save()       
        messages.success(request, f'Notes added from {request.user.username} succesfully')
        return redirect('/notes/')

    form = NoteForm()
    note = Notes.objects.filter(user = request.user)
    return render(request, 'dashboard/notes.html', context = {'Notes': note, 'form': form})


@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('/notes/')


@login_required
def note_info(request, pk):
    note = Notes.objects.get(id=pk)
    referer = request.META.get('HTTP_REFERER', '/')
    return render(request, 'dashboard/notes_detail.html', context={'notes': note, 'referer': referer})

# class note_details(generic.DetailView):
#     model = Notes


@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get('status')
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            
            user = request.user
            subject = request.POST.get('subject')
            title = request.POST.get('title')
            description = request.POST.get('description')
            due = request.POST.get('due')
            hw = Homework(user=user, subject=subject, title=title, description=description, due=due, status=finished)
            hw.save()

        messages.success(request, f'Homework added from {request.user.username} succesfully')
        return redirect('/homework/')

    form = HomeworkForm()
    hw = Homework.objects.filter(user=request.user)
    if len(hw) == 0:
        hw_done = True
    else:
        hw_done = False
    
    context = {
        'homework' : hw, 
        'hw_done' : hw_done, 
        'form' : form
    }
    return render(request,'dashboard/homework.html', context = context)


@login_required
def update_hw(request, pk=None):
    hw = Homework.objects.get(id=pk)
    if hw.status == True:
        hw.status = False
    else:
        hw.status = True
    hw.save()

    return redirect('/homework/')


@login_required
def delete_hw(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('/homework/')



def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text')
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'viewcount' : i['viewCount']['short'],
                'published' : i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)

            context={
                'form': form,
                'results': result_list
            }
        
        return render(request, 'dashboard/youtube.html', context=context)
    
    form = DashboardForm()
    context={'form': form}
    return render(request, 'dashboard/youtube.html', context=context)


@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get('status')
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            
            user = request.user
            title = request.POST.get('title')
            time = request.POST.get('time')
            todo = ToDo(user=user, title=title, time=time, status=finished)
            todo.save()
        
        messages.success(request, f'Todo item added from {request.user.username} succesfully')
        return redirect('/todo/')

    form = TodoForm()
    todo = ToDo.objects.filter(user=request.user).order_by('time')
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    
    context = {
        'Todo' : todo, 
        'todo_done' : todo_done, 
        'form' : form
    }
    return render(request,'dashboard/todo.html', context=context)


@login_required
def update_todo(request, pk=None):
    todo = ToDo.objects.get(id=pk)
    if todo.status == True:
        todo.status = False
    else:
        todo.status = True
    todo.save()
    referer = request.META.get('HTTP_REFERER', '/')
    # url = request.url
    print(referer)

    return redirect('/todo/')


@login_required
def delete_todo(request, pk=None):
    ToDo.objects.get(id=pk).delete()
    return redirect('/todo/')



def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Accounted cretaed for {username}')
        return redirect('/login/')

    form = UserRegistration()
    context={'form': form}
    return render(request, 'dashboard/register.html', context=context)

 
@login_required
def profile(request):
    todo = ToDo.objects.filter(user = request.user, status = False).order_by('time')
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    hw = Homework.objects.filter(user = request.user, status = False)
    if len(hw) == 0:
        hw_done = True
    else:
        hw_done = False

    context = {
        'Todo' : todo, 
        'todo_done' : todo_done,
        'homework' : hw, 
        'hw_done' : hw_done
    }
    return render(request, 'dashboard/profile.html', context=context)