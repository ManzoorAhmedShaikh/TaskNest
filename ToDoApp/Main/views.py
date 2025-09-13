from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Notes
import json
from django.utils.timezone import make_aware
from datetime import datetime

def login(request):
    if request.method == "POST":
        if request.POST.get('action') == "logout":
            auth.logout(request)
            return redirect('/')

        username = request.POST["user"]
        password = request.POST["password"]

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')

        else:
            error = "Invalid credentials, try again."
            return render(request, 'login.html', context= {"error": error})

    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST" and request.POST.get('action') == 'user_registration':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if len(password) < 8:
            error = "Password must be at least 8 characters long."
            return render(request, 'register.html', context= {"error": error})

        elif password != password2:
            error = "Passwords do not match."
            return render(request, 'register.html', context= {"error": error})

        elif User.objects.filter(username = username).exists():
            error = f"User: '{username}' already exist, try another name."
            return render(request, 'register.html', context= {"error": error})

        elif User.objects.filter(email=email).exists():
            error = f"Email: '{email}' already taken, try another name."
            return render(request, 'register.html', context={"error": error})

        User.objects.create_user(username=username, email=email, password=password)
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return redirect('/home')

    else:
        return render(request, 'register.html')

def main(request):
    notes = Notes.objects.filter(username = request.user)

    if request.method == "POST":
        data = json.loads(request.body)
        print("Something coming")
        if data.get('action') == 'add':
            note = Notes.objects.create(username = request.user, note_name = data.get('note_name'), note_status = data.get('note_status'), note_date = make_aware(datetime.strptime(data.get('note_date'), "%Y-%m-%d")))
            return JsonResponse({'success': True, 'id': note.id})

        elif data.get('action') == 'update':
            note = Notes.objects.get(id=data.get("id"), username=request.user)
            note.note_status = True if data.get("status") == "Active" else False
            note.save()
            return JsonResponse({'success': True, 'id': note.id})

    else:
        return render(request, 'home.html', context = {'notes': notes})
