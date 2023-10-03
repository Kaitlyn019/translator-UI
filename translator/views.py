from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def room(request, room_name):
    if room_name == 'client':
        return render(request, 'client.html', {
            'room_name': 'test'
        })
    else:
        return render(request, 'server.html', {
            'room_name': 'test'
        })
