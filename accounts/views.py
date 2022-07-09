from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm,ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
User=get_user_model()
from scraping.models import Error

def login_view(request):
    if not request.user.is_authenticated:
        form =UserLoginForm(request.POST or None)
        if form.is_valid():
            data=form.cleaned_data
            email=data.get('email')
            password=data.get('password')
            user=authenticate(request,email=email,password=password)
            login(request,user)
            return redirect('home')

        return render(request,'accounts/login.html',{'form':form})
    else:
        return redirect('home')
def log_out(request):
    logout(request)
    return redirect('login')


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user=form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request,"Success!")
        return render(request,'accounts/register_done.html',{'new_user':new_user})
    return render(request,'accounts/register.html',{'form':form})


def update_view(request):
    contact_form=ContactForm()
    if request.user.is_authenticated:
        user=request.user
        if request.method=='POST':
            form=UserUpdateForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                user.city=data['city']
                user.language=data['language']
                user.send_email=data['send_email']
                user.save()
                messages.success(request, "Profile was updated!")
                return redirect('update')
        form=UserUpdateForm(initial={'city':user.city,'language':user.language,'send_email':user.send_email})
        return render(request, 'accounts/update.html', {'form': form,'contact_form':contact_form})

    else:
        return redirect('login')

def contact(request):
    if request.method=='POST':
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
            data=contact_form.cleaned_data
            city=data.get('city')
            language=data.get('language')
            email=data.get('email')
            qs = Error.objects.filter(timestamp=datetime.today())
            if qs.exists():
                err = qs.first()
                data=err.data.get('user_data',[])
                data.append({'city':city,'language':language,'email':email})
                err.data['user_data']=data
                err.save()
            else:
                data=[{'city':city,'language':language,'email':email}]
                Error(data=f"user_data:{data}").save()
            messages.success(request, "Request has been sent")
            return redirect('update')
        else:
            return redirect('update')
    else:
        return redirect('login')

def delete_view(request):
    if request.user.is_authenticated:
        user=request.user
        if request.method=='POST':
            qs=User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, "Profile was deleted!!")
    return redirect('home')