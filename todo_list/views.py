from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ListForm(request.POST or None)
            if form.is_valid():
                form.save()

            #if request.user.is_authenticated:
                #all_items = List.objects.all
                #user_id = request.user
                #print(user_id)
                #all_items = List.objects.filter(user=user_id.id)
                messages.success(request, ('Item Added Successfully !'))
                #return render(request, 'home.html', { 'all_items' : all_items})
                return redirect('home')
        else:

            user_id = request.user
            all_items = List.objects.filter(user=user_id.id)
            if all_items :
                return render(request, 'home.html', { 'all_items' : all_items})
            else:
                messages.error(request, ("No items to show"))
                return render(request, 'home.html', {})
def about(request):
    all_items = List.objects.all
    return render(request, 'about.html', { 'all_items' : all_items })

def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    if item.user != request.user:
        messages.warning(request, ('You are not authorised to change this item'))
        return redirect('home')
    else:
        item.delete()
        messages.success(request, ('Item Deleted Successfully !'))
        return redirect('home')


def completed(request, list_id):                    #use it as toggle
    item = List.objects.get(pk=list_id)
    if item.user != request.user:
        messages.warning(request, ('You are not authorised to change this item'))
        return redirect('home')
    else:
        item.completed = True
        item.save()
        return redirect('home')

def not_completed(request, list_id):    #use it as toggle
    item = List.objects.get(pk=list_id)
    if item.user != request.user:
        messages.warning(request, ('You are not authorised to change this item'))
        return redirect('home')
    else:
        item.completed = False
        item.save()
        return redirect('home')

def edit(request, list_id):
    if request.method == 'POST':
        item = List.objects.get(pk=list_id)
        id = item.user
        if id == request.user:
            form = ListForm(request.POST or None, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, ('Item edited Successfully !'))
                return redirect('home')
        else :
            messages.warning(request, ('You are not authorised to change this item'))
            return redirect('home')

    else:
        item = List.objects.get(pk=list_id)
        if item.user != request.user:
            messages.warning(request, ('You are not authorised to change this item'))
            return redirect('home')
        else:
            return render(request, 'edit.html', { 'item' : item})

def edt_prf(request):
    if request.method == 'POST':
        user = User.objects.get(pk = request.user.id)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        if user.check_password(password):
            if User.objects.filter(username=username).exists() and username != user.username:
                messages.warning(request, ('Username Already exist'))
                return redirect('edt_prf')
            elif User.objects.filter(email=email).exists()  and email != request.user.email:
                messages.warning(request, ('Email Already exist'))
                return redirect('edt_prf')
            else:
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.username = username
                user.email = email
                user.save()
                messages.success(request, ('Your profile updated Successfully !'))
                return redirect('home')
        else:
            messages.warning(request, ('Your password is incorrect, Please enter correct password!'))
            return redirect('edt_prf')

    else:
        return render(request, 'edt_prf.html', {})



def ch_pass(request):
    if request.method == 'POST':
        user = User.objects.get(pk = request.user.id)
        old_pass = request.POST['old_pass']
        if user.check_password(old_pass):
            new_pass = request.POST['new_pass']
            if new_pass == request.POST['password']:
                user.set_password(new_pass)
                print(user.password)
                user.save()
                messages.success(request, ('Password updated Successfully'))
                auth.logout(request)
                return redirect('/')
            else:
                messages.warning(request, ('New password and confirm password are not same'))
        else:
            messages.warning(request, ('Enter correct old password'))
            return redirect('ch_pass')
    else:
        return render(request, 'ch_pass.html', {})
