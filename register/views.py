from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.views.decorators.csrf import csrf_exempt


def pageProfile(request):
    return render(request, 'profile.html')

def pageSettings(request):
    return render(request, 'profile-edit.html')

@csrf_exempt
def pageSignup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro'yhatdan o'tdingiz!" )
            return redirect("home")
        messages.error(request, "Iltimos, Malumotlar to'g'ri kiritilganligini tekshiring")
        
    form = NewUserForm()
    return render (request=request, template_name="sign-up.html", context={"register_form":form})

@csrf_exempt
def pageSignin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Siz muvaffaqiyatli kirishga erishdingiz {username}.")
                return redirect("home")
            else:
                messages.error(request,"Username yoki Parol noto'g'ri kiritildi")
        else:
            messages.error(request,"Username yoki Parol noto'g'ri kiritildi")
    form = AuthenticationForm()
    return render(request=request, template_name="sign-in.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	return redirect("sign_in")