from django.shortcuts import render,redirect,get_object_or_404
from .forms import CreateUserForm,LoginForm,CreateRecordForm,UpdateRecordForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Record
from django.db.models import Q
import logging
from django.contrib import messages

def index(request):
    return render(request, 'web/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request , 'successfully registered')
            return redirect('login')
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
                messages.success(request , 'successfully logined')
                return redirect('dashboard') 
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'web/login.html', context)

@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()
    return render(request, 'web/dashboard.html' , context={'records':records})

def my_logout(request):
    logout(request)
    messages.success(request , 'successfully logout')

    return redirect('login')

@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request , 'successfully created record')

            return redirect('dashboard')
    else:
        form = CreateRecordForm()
    context = {'form':form}
    return render(request,'web/create-record.html',context=context)

@login_required(login_url='login')
def view_record(request, record_id):
    all_records = get_object_or_404(Record, id = record_id)
    context ={
        'records':all_records
    }
    return render(request,'web/view-record.html',context=context)

@login_required(login_url='login')
def update_record(request, record_id):
    record = get_object_or_404(Record, id = record_id)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            messages.success(request , 'successfully updated record')
            
            return redirect('dashboard')
    
    context = {'form':form}
    return render(request,'web/update-record.html',context=context)


@login_required(login_url='login')
def delete_record(request, record_id):
    record = get_object_or_404(Record, id = record_id)
    record.delete()
    messages.success(request , 'successfully deleted record')
   
    return redirect('dashboard')
    
logger = logging.getLogger(__name__)
@login_required(login_url='login')
def search(request):
    query = request.GET.get('query')
    results = []
    try:
        if query:
            results = Record.objects.filter(Q(first_name__icontains=query) | Q(id__icontains=query))
    except Exception as e:
        logger.error('Error during search:  %s',e)
    return render(request , 'web/search.html' , context={'results' : results , 'query':query})


def custom_page_not_found(request, exception):
    return render(request , 'web/404.html' , status=404)