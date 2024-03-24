from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
from .forms import RegisterForm, AuthForm, BuildingForm
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
import json
import threading

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# Remove after testing
import time

def html_email(building,address,unit,name,phone,entry,request,recipient,subject):
    sender_email = "cs423robot@gmail.com" 
    recipient_email = recipient
    #subject = "Maintenance Request"
    dashboard = "https://tanrtech.com/dashboard/"
    today = str(date.today())
    
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    if(entry):
        enter = "Yes"
    else: 
        enter = "No"

    # write the text/plain part
    text = """\
    Hello, a new maintenance request has been made on """ + today + """
    Building: """ + building + """
    Address: """ + address + """
    Unit: """ + unit + """
    Resident Name: """ + name + """
    Phone: """ + phone + """
    Request:""" + request + """
    Can we enter without resident present: """ + enter 

    
    # write the HTML part
    html = """\
    <html>
    <style>
  table {
    border-collapse: collapse;
  }
</style>

<table>
  <tr>
    <td>Building:</td>
    <td><strong>""" + building + """</strong></td>
  </tr>
  <tr>
    <td>Address:</td>
    <td><strong>""" + address + """</strong></td>
  </tr>
  <tr>
    <td>Unit:</td>
    <td><strong>""" + unit + """</strong></td>
  </tr>
  <tr>
    <td>Resident Name:</td>
    <td><strong>""" + name + """</strong></td>
  </tr>
  <tr>
    <td>Phone:</td>
    <td><strong>""" + phone + """</strong></td>
  </tr>
  <tr>
    <td width:50px>Can we enter without<br> a resident present:</td>
    <td><strong>""" + enter + """</strong></td>
  </tr>
  <tr>
    <td>Request:</td>
    <td><strong>""" + request + """</strong></td>
  </tr>
  
</table>

    </html>
    """

    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)       


    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, "tjcm gvmf ilvq jnqy") 
        server.sendmail(sender_email, recipient_email, message.as_string())

def send_email_thread(building_id, address, unit, full_name, phone, entry_permission, req, recipient_email, subject):
    email_thread = threading.Thread(target=html_email, args=(building_id, address, unit, full_name, phone, entry_permission, req, recipient_email, subject))
    email_thread.start()
    
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'home.html')

def support(request):
    return render(request, 'support.html')

@login_required(login_url="/login")
def dashboard(request):
    if request.user.is_superuser:
        return admin_dashboard(request)
    elif request.user.manager != None:
        return manager_dashboard(request)
    else:
        return tenant_dashboard(request)
    
@login_required(login_url="/login")
def admin_dashboard(request):
    users = UserAccount.objects.all()
    maintenance_requests = MaintenanceRequest.objects.all()
    buildings = Building.objects.all()
    per_page = 10
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html', {'users': users, 'maintenance_requests': maintenance_requests, 'buildings': buildings})
    else:
        return handler_403(request)

@login_required(login_url="/login")
def manager_dashboard(request):
    users = UserAccount.objects.all()
    maintenance_requests = MaintenanceRequest.objects.all()
    per_page = 10
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.user.manager != None:
        return render(request, 'dashboard/manager_dashboard.html', {'users':users, 'maintenance_requests':maintenance_requests})
    else:
        return handler_403(request)

@login_required(login_url="/login")
def tenant_dashboard(request):
    maintenance_requests = MaintenanceRequest.objects.filter(userId=request.user.id)

    return render(request, 'dashboard/tenant_dashboard.html', {'maintenance_requests':maintenance_requests})
    
@login_required(login_url="/login")
def users(request):
    return redirect('/dashboard')

@login_required(login_url="/login")
def maintenance_requests(request):
    if request.user.is_superuser or (request.user.manager != None):
        search_query = request.GET.get('search_query')
        if search_query:
            maintenance_requests = MaintenanceRequest.objects.filter(
                Q(id__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(building__buildingName__icontains=search_query) |
                Q(unit__icontains=search_query) |
                Q(entry_permission__icontains=search_query)
            )
        else:
            maintenance_requests = MaintenanceRequest.objects.all()

        html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': maintenance_requests})
        if request.headers.get('HX-Request'):
            #time.sleep(2)
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/maintenance_requests.html')
    else:
        return handler_403(request)

@login_required(login_url="/login")
def maintenance(request):
    buildings = Building.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = first_name + " " + last_name
        address = request.POST.get('address')
        unit = request.POST.get('unit')
        title = request.POST.get('title')
        req = request.POST.get('request')
        phone = request.POST.get('phone')
        building_id = request.POST.get('building')
        building = Building.objects.get(id=building_id)
        entry_permission = request.POST.get('entry_permission') == '1'
        send_email_thread(building_id,address,unit,full_name,phone,entry_permission,req,"cs423robot@gmail.com","Maintenance Request")
        send_email_thread(building_id,address,unit,full_name,phone,entry_permission,req,request.user.email,"Maintenance Request Confirmation")
        maintenanceRequest = MaintenanceRequest.objects.create(userId=request.user, first_name=first_name, last_name=last_name, address=address, unit=unit, request=req, phone=phone, building=building, entry_permission=entry_permission, title=title)
        return redirect('/request/' + str(maintenanceRequest.id))

    return render(request, 'forms/maintenance/maintenance.html', {'buildings': buildings})

@login_required(login_url="/login")
def user_profile(request, username):
    return render(request, 'profile.html', {'user_profile' : username})

@login_required(login_url="/login")
def building_info(request, building_id):
    if request.user.is_superuser or request.user.manager != None:
        building = get_object_or_404(Building, pk=building_id)
        maintenance_requests = MaintenanceRequest.objects.filter(building=building)
        return render(request, 'dashboard/data/building_info.html', {'building': building, 'maintenance_requests': maintenance_requests})
    else:
        return handler_403(request)


@login_required(login_url="/login")
def edit_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    buildings = Building.objects.all()
    if request.method == 'POST':
        maintenance_request.first_name = request.POST.get('first_name', maintenance_request.first_name)
        maintenance_request.last_name = request.POST.get('last_name', maintenance_request.last_name)
        maintenance_request.unit = request.POST.get('unit', maintenance_request)
        maintenance_request.title = request.POST.get('title', maintenance_request.title)
        maintenance_request.request = request.POST.get('request', maintenance_request.request)
        maintenance_request.entry_permission = request.POST.get('entry_permission', maintenance_request.entry_permission)
        maintenance_request.phone = request.POST.get('phone', maintenance_request.phone)
        maintenance_request.entry_permission = request.POST.get('entry_permission', maintenance_request)
        maintenance_request.status = request.POST.get('status', maintenance_request.status)
        building_id = request.POST.get('building')
        building = get_object_or_404(Building, pk=building_id)
        maintenance_request.building = building

        if request.user.is_superuser or request.user.manager:
            if (maintenance_request.dateCompleted is not None):
                maintenance_request.dateCompleted = None

        maintenance_request.save()
        return redirect('request_info', request_id=maintenance_request.id)

    return render(request, 'dashboard/data/edit_request.html',
                  {'maintenance_request': maintenance_request, 'buildings': buildings})


def edit_note(request, note_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            note_id = data.get('note_id')
            new_note_text = data.get('note_text')
            if new_note_text is None:
                return JsonResponse({'success': False, 'error': 'no note text provided'})
            note = get_object_or_404(MaintenanceNotes, pk=note_id)
            note.notes = new_note_text
            note.save()
            return JsonResponse({'success': True})
    else:
        return handler_403(request)


def delete_note(request, note_id):
    if request.method == 'POST':
        note_to_delete = get_object_or_404(MaintenanceNotes, id=note_id)
        note_to_delete.delete()
        return JsonResponse({'success': True})
    else:
        return handler_403(request)


@login_required(login_url="/login")
def request_info(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    if request.user.is_superuser or request.user.manager != None or request.user == maintenance_request.userId:
        can_edit_request = (request.user.is_superuser or request.user.manager)
        return render(request, 'dashboard/data/request_info.html', {'maintenance_request': maintenance_request, 'can_edit_request': can_edit_request})
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def view_user(request, username):
    u = get_object_or_404(UserAccount, username=username)
    if request.user.is_superuser:
        if request.method == 'POST':
            data = json.loads(request.body)
            updated_first_name = data.get('first_name')
            updated_last_name = data.get('last_name')
            updated_username = data.get('username')
            updated_email = data.get('email')
            account_type = data.get('account_type')

            u.first_name = updated_first_name
            u.last_name = updated_last_name
            u.username = updated_username
            u.email = updated_email
            u.setAccountType(account_type)
            u.save()

            return JsonResponse({'message': 'Profile updated successfully'})
            
        return render(request, 'dashboard/pages/view_user.html', {'u': u})
    else:
        return handler_403(request)

def add_note(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    notes = request.POST.get('notes')
    if request.method == 'POST' and request.user.is_superuser or request.user.manager != None:
        new_note = MaintenanceNotes(
            maintenanceRequestId = maintenance_request,
            userId = request.user,
            dateMade = timezone.now(),
            notes = notes
        )
        new_note.save()
        return redirect('request_info', request_id=request_id)
    else:
        return handler_403(request)

@login_required(login_url="/login")
def add_building(request):
    user = request.user
    if user.is_superuser:
        form = BuildingForm()
        if request.method == 'POST':
            form = BuildingForm(request.POST)
            if form.is_valid():
                form.save()
                return dashboard(request)
        return render(request, 'dashboard/forms/create_building.html', {'form': form})
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        updated_first_name = data.get('first_name')
        updated_last_name = data.get('last_name')
        updated_username = data.get('username')
        updated_email = data.get('email')

        user = request.user
        user.first_name = updated_first_name
        user.last_name = updated_last_name
        user.username = updated_username
        user.email = updated_email
        user.save()

        return JsonResponse({'message': 'Profile updated successfully'})
    
    return render(request, 'profile.html')

# Views for user account authentication
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                request.session.set_expiry(0) # Set session to expire when brower is closed
                return redirect('/')
        else:
            form = RegisterForm()
        
        return render(request, 'registration/signup.html', {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            form = AuthForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session.set_expiry(0) # Set session to expire when brower is closed
                    next_url = request.GET.get('next', None)
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('/dashboard')
        else:
            form = AuthForm(request)
            
        return render(request, 'registration/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')


# Views for handling deleting
@login_required(login_url="/login")
def delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data.get('type')
        id_num = data.get('id')

        if type == "UserAccount":
            if request.user.is_superuser or request.user.id == id_num:
                try:
                    u = UserAccount.objects.get(pk=id_num)
                    u.delete()
                    return JsonResponse({'success': True})
                except UserAccount.DoesNotExist:
                    return JsonResponse({'success': False})
                
        elif type == "MaintenanceRequest":
            if request.user.is_superuser:
                try:
                    request = MaintenanceRequest.objects.get(pk=id_num)
                    request.delete()
                    return JsonResponse({'success': True})
                except MaintenanceRequest.DoesNotExist:
                    return JsonResponse({'success': False})
                
        elif type == "Building":
            if request.user.is_superuser:
                try:
                    building = Building.objects.get(pk=id_num)
                    building.delete()
                    return JsonResponse({'success': True})
                except Building.DoesNotExist:
                    return JsonResponse({'success': False})
                

# Views for errors
def handler_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def handler_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler_500(request):
    return render(request, 'errors/500.html', status=500)