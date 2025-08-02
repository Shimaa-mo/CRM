from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request, 'web/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('login')
        else:
            form = CreateUserForm()

    context = {'form' : form}
    return render(request , "web/register.html",context)


def my_login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard') 
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'web/login.html', context)

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'web/dashboard.html')

def my_logout(request):
    logout(request)
    return redirect('login')
    