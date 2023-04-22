from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = room.count()
    context = {'rooms': room, 'topics': topics, 'room_count': room_count}
    return render(request, 'main/home.html', context)

def rom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'rooms': room}
    return render(request, 'main/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form': form}
    return render(request, 'main/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form' : form}
    return render(request, 'main/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('Home')

    context = {'obj' : room}
    return render(request, 'main/delete.html', context)