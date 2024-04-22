from django.db.models import Q, Count
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
from django.core.exceptions import ValidationError
import json
import threading
from email.mime.image import MIMEImage

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# Remove after testing
import time
import os
import mimetypes

def html_email(building_name,unit,name,phone,entry,title,request,recipient,subject, images=None):
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

    if images:
        for image_path in images:
            with open(image_path, 'rb') as image_file:
                img_data = image_file.read()
                img_mime_type, _ = mimetypes.guess_type(image_path)
                img_mime_subtype = img_mime_type.split('/')[-1] if img_mime_type else 'octet-stream'
                img = MIMEImage(img_data, _subtype=img_mime_subtype)
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                message.attach(img)

    # write the text/plain part
    text = """\
    Hello, a new maintenance request has been made on """ + today + """
    Building: """ + building_name + """
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
    <td><strong>""" + building_name + """</strong></td>
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
    <td>Title:</td>
    <td><strong>""" + title + """</strong></td>
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

def send_email_thread(building_name, unit, full_name, phone, entry_permission, title, req, recipient_email, subject, images):
    email_thread = threading.Thread(target=html_email, args=(building_name, unit, full_name, phone, entry_permission, title, req, recipient_email, subject, images))
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
    elif request.user.is_manager:
        return manager_dashboard(request)
    else:
        return tenant_dashboard(request)
    
@login_required(login_url="/login")
def admin_dashboard(request):
    users = UserAccount.objects.all()
    maintenance_requests = MaintenanceRequest.objects.order_by('-id')[:10]
    buildings = Building.objects.all().order_by("id")
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
    users = UserAccount.objects.all().order_by('id')
    maintenance_requests = MaintenanceRequest.objects.order_by('-id')[:10]
    buildings = Building.objects.all().order_by("id")
    per_page = 10
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.user.is_manager:
        return render(request, 'dashboard/manager_dashboard.html', {'users':users, 'maintenance_requests':maintenance_requests, 'buildings': buildings})
    else:
        return handler_403(request)

@login_required(login_url="/login")
def tenant_dashboard(request):
    maintenance_requests = MaintenanceRequest.objects.filter(user_id=request.user.id)

    return render(request, 'dashboard/tenant_dashboard.html', {'maintenance_requests':maintenance_requests})
    
@login_required(login_url="/login")
def users(request):
    if request.user.is_superuser or request.user.is_manager:
        search_query = request.GET.get('search_query')
        if search_query:
            users = UserAccount.objects.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            ).order_by('id')
        else:
            users = UserAccount.objects.all().order_by('id')

        html = render_to_string('dashboard/data/users_htmx.html', {'users': users})
        if request.headers.get('HX-Request'):
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/users.html')
    else:
        return handler_403(request)

@login_required(login_url="/login")
def buildings(request):
    if request.user.is_superuser or request.user.is_manager:
        search_query = request.GET.get('search_query')
        if search_query:
            buildings = Building.objects.filter(
                Q(building_name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(state__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(zipcode__icontains=search_query)
            ).order_by('id')
        else:
            buildings = Building.objects.all().order_by('id')

        html = render_to_string('dashboard/data/buildings_htmx.html', {'buildings': buildings})
        if request.headers.get('HX-Request'):
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/buildings.html')
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def maintenance_requests(request):
    if request.user.is_superuser or request.user.is_manager:
        search_query = request.GET.get('search_query')
        if search_query:
            maintenance_requests = MaintenanceRequest.objects.filter(
                Q(id__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(building__building_name__icontains=search_query) |
                Q(unit__icontains=search_query) |
                Q(entry_permission__icontains=search_query)
            ).order_by('id')
        else:
            maintenance_requests = MaintenanceRequest.objects.all().order_by('id')

        html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': maintenance_requests})
        if request.headers.get('HX-Request'):
            #time.sleep(2)
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/maintenance_requests.html')
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def saved_requests(request):
    search_query = request.GET.get('search_query')
    if search_query:
        maintenance_requests = MaintenanceRequest.objects.filter(
            Q(id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(building__building_name__icontains=search_query) |
            Q(unit__icontains=search_query) |
            Q(entry_permission__icontains=search_query),
            useraccountmaintenancerequest__user_id=request.user
        ).order_by('id')
    else:
        maintenance_requests = MaintenanceRequest.objects.filter(
            useraccountmaintenancerequest__user_id=request.user
        ).order_by('id')

    html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': maintenance_requests})
    if request.headers.get('HX-Request'):
        return HttpResponse(html)
    else:
        return render(request, 'dashboard/pages/saved_requests.html')
    


@login_required(login_url="/login")
def sort_requests(request):
    search_query = request.GET.get('search_query')
    sort_by = request.GET.get('sort_by', 'id')  # Default sorting is by 'id'
    if search_query:
        maintenance_requests = MaintenanceRequest.objects.filter(
            Q(id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(building__building_name__icontains=search_query) |
            Q(unit__icontains=search_query) |
            Q(entry_permission__icontains=search_query)
        ).order_by(sort_by)
    else:
        maintenance_requests = MaintenanceRequest.objects.all().order_by(sort_by)

    html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': maintenance_requests})
    return HttpResponse(html)

@login_required(login_url="/login")
def maintenance(request):
    buildings = Building.objects.all().order_by("id")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = first_name + " " + last_name
        unit = request.POST.get('unit')
        title = request.POST.get('title')
        req = request.POST.get('request')
        phone = request.POST.get('phone')
        building_id = request.POST.get('building')
        date_submitted = timezone.now()
        building = Building.objects.get(id=building_id)
        priority = request.POST.get('priority')
        entry_permission = request.POST.get('entry_permission') == '1'
        images = request.FILES.getlist('images')

        maintenanceRequest = MaintenanceRequest.objects.create(user_id=request.user, first_name=first_name,
                                                               last_name=last_name, unit=unit, request=req, phone=phone,
                                                               building=building, priority=priority,
                                                               entry_permission=entry_permission, title=title,
                                                               date_submitted=date_submitted)

        image_paths = []

        for image in images:
            maintenance_file = MaintenanceFile.objects.create(maintenanceRequestId=maintenanceRequest, file=image)
            image_paths.append(maintenance_file.file.path)

        send_email_thread(building.building_name,unit,full_name,phone,entry_permission,title, req,"cs423robot@gmail.com","Maintenance Request", image_paths)
        send_email_thread(building.building_name,unit,full_name,phone,entry_permission,title, req,request.user.email,"Maintenance Request Confirmation", image_paths)

        # Send to users with email notifications on
        users_with_notifications = UserAccount.objects.filter(email_notifications=True)
        for user in users_with_notifications:
            if (user.is_superuser or user.is_manager) and user != request.user:
                send_email_thread(building.building_name,unit,full_name,phone,entry_permission,title, req,user.email,"Maintenance Request Notification")

        return redirect('/request/' + str(maintenanceRequest.id))

    return render(request, 'dashboard/create/maintenance.html', {'buildings': buildings})

@login_required(login_url="/login")
def building_info(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.user.is_superuser or request.user.is_manager:
        if request.method == 'POST':
            if request.user.is_superuser:
                data = json.loads(request.body)
                building.building_name = data.get('name')
                building.address = data.get('address')
                building.city = data.get('city')
                building.state = data.get('state')
                building.country = data.get('country')
                building.zipcode = data.get('zipcode')

                try:
                    building.full_clean()  # This will run all validators on the model fields
                    building.save()
                    return JsonResponse({'message': 'Profile updated successfully'})
                except ValidationError as e:
                    # Handle the validation error, e.g., return an error response
                    return JsonResponse({'errors': e.message_dict}, status=400)
            else:
                 return JsonResponse({'errors': 'Not authorized'}, status=403)
            
        maintenance_requests = MaintenanceRequest.objects.filter(building=building)
        return render(request, 'dashboard/info/building_info.html', {'building': building, 'maintenance_requests': maintenance_requests})
    else:
        return handler_403(request)

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
    maintenance_files = MaintenanceFile.objects.filter(maintenanceRequestId=maintenance_request)
    if request.user.is_superuser or request.user.is_manager:
        buildings = Building.objects.all().order_by("id")
        if request.method == 'POST':
            data = json.loads(request.body)
            maintenance_request.first_name  = data.get('first_name')
            maintenance_request.last_name = data.get('last_name')
            maintenance_request.phone = data.get('phone')
            maintenance_request.building = get_object_or_404(Building, pk=data.get('building'))
            maintenance_request.unit = data.get('unit')
            maintenance_request.status = data.get('status')
            maintenance_request.priority = data.get('priority')
            maintenance_request.title = data.get('title') 
            maintenance_request.request = data.get('request')
            maintenance_request.entry_permission = data.get('entry_permission')

            try:
                maintenance_request.full_clean()
                maintenance_request.save()
                return JsonResponse({'message': 'Profile updated successfully'})
            except ValidationError as e:
                # Handle the validation error, e.g., return an error response
                return JsonResponse({'errors': e.message_dict}, status=400)

        can_edit_request = (request.user.is_superuser or request.user.is_manager)
        maintenance_notes = maintenance_request.maintenance_notes.all()
        saved = request_is_saved(request, request_id)
        return render(request, 'dashboard/info/request_info.html', {'maintenance_request': maintenance_request, 'maintenance_files': maintenance_files, 'buildings': buildings,'can_edit_request': can_edit_request, 'maintenance_notes': maintenance_notes, 'saved': saved})
    elif request.user == maintenance_request.user_id:
        can_edit_request = (request.user.is_superuser or request.user.is_manager)
        maintenance_notes = maintenance_request.maintenance_notes.filter(tenant_viewable=True)
        saved = request_is_saved(request, request_id)
        return render(request, 'dashboard/info/request_info.html',
                      {'maintenance_request': maintenance_request, 'maintenance_files': maintenance_files, 'can_edit_request': can_edit_request,'maintenance_notes': maintenance_notes, 'saved': saved})
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def user_info(request, username):
    u = get_object_or_404(UserAccount, username=username)
    if request.user.is_superuser or request.user.is_manager:
        if request.method == 'POST':
            if request.user.is_superuser:
                data = json.loads(request.body)
                u.first_name = data.get('first_name')
                u.last_name = data.get('last_name')
                u.username = data.get('username')
                u.email = data.get('email')
                u.setAccountType(data.get('account_type'))

                try:
                    u.full_clean()  # This will run all validators on the model fields
                    u.save()
                    return JsonResponse({'message': 'Profile updated successfully'})
                except ValidationError as e:
                    # Handle the validation error, e.g., return an error response
                    return JsonResponse({'errors': e.message_dict}, status=400)
            else:
                return JsonResponse({'errors': 'Not authorized'}, status=403)
        maintenance_requests = MaintenanceRequest.objects.filter(user_id=u)
        return render(request, 'dashboard/info/user_info.html', {'u': u, 'maintenance_requests' :maintenance_requests})
    else:
        return handler_403(request)

def add_note(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    notes = request.POST.get('notes')
    is_tenant_viewable = 'is_tenant_viewable' in request.POST
    if request.method == 'POST' and request.user.is_superuser or request.user.is_manager:
        new_note = MaintenanceNotes(
            maintenanceRequestId = maintenance_request,
            user_id = request.user,
            date_submitted = timezone.now(),
            notes = notes,
            tenant_viewable = is_tenant_viewable
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
        return render(request, 'dashboard/create/create_building.html', {'form': form})
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.user.first_name = data.get('first_name')
        request.user.last_name = data.get('last_name')
        request.user.username = data.get('username')
        request.user.email = data.get('email')
        request.user.email_notifications = data.get('email_notifications')

        try:
            request.user.full_clean()  # This will run all validators on the model fields
            request.user.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        except ValidationError as e:
            # Handle the validation error, e.g., return an error response
            return JsonResponse({'errors': e.message_dict}, status=400)
    
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

def request_is_saved(request, request_id):
    try:
        existing_relationship = UserAccountMaintenanceRequest.objects.get(
            user_id=request.user, maintenanceRequest_id=MaintenanceRequest.objects.get(pk=request_id)
        )
        return True
    except UserAccountMaintenanceRequest.DoesNotExist:
        return False
    
def check_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username').lower()
        if UserAccount.objects.filter(username=username).exists():
            return JsonResponse({'taken': True})
        else:
            return JsonResponse({'taken': False})
    else:
        return handler_404(request)
    
@login_required(login_url="/login")
def toggle_save(request, request_id):
    if request.method == 'POST':
        maintenance_request = MaintenanceRequest.objects.get(pk=request_id)
        if (request.user.is_superuser or request.user.is_manger or request.user == maintenance_request.user_id):
            try:
                existing_relationship = UserAccountMaintenanceRequest.objects.get(
                    user_id=request.user, maintenanceRequest_id=maintenance_request
                )
                existing_relationship.delete()
                return JsonResponse({'saved': False})
            except UserAccountMaintenanceRequest.DoesNotExist:
                new_relationship = UserAccountMaintenanceRequest.objects.create(
                    user_id=request.user, maintenanceRequest_id=maintenance_request
                )
                new_relationship.save()
                return JsonResponse({'saved': True})
    else:
        return handler_404(request, None)

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
            if request.user.is_superuser or request.user.is_manager:
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
    else:
        return handler_404(request)
                
@login_required(login_url='/login')
def advanced_search(request):
    if request.user.is_superuser or request.user.is_manager:
        search_option = request.GET.get('search_option')

        if search_option == "user_accounts":
            return search_user_accounts(request)
        elif search_option == "buildings":
            return search_buildings(request)
        elif search_option == "maintenance_requests":
            return search_maintenance_requests(request)
        else:
            return render(request, 'dashboard/pages/advanced_search.html')
    else:
        return handler_403(request)


def search_user_accounts(request):
    search_query = request.GET.get('search_query')

    users = UserAccount.objects.filter(
        Q(username__icontains=search_query) |
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) |
        Q(email__icontains=search_query)
    )

    html_content = render_to_string('dashboard/data/user.html', {'users': users})

    return JsonResponse({'html_content': html_content})

@login_required(login_url='/login')
def search_buildings(request):
    search_query = request.GET.get('search_query')

    buildings = Building.objects.filter(
        Q(building_name__icontains=search_query) |
        Q(address__icontains=search_query) |
        Q(city__icontains=search_query) |
        Q(state__icontains=search_query) |
        Q(country__icontains=search_query) |
        Q(zipcode__icontains=search_query)
    )
    html_content = render_to_string('dashboard/data/building.html', {'buildings': buildings})

    return JsonResponse({'html_content': html_content})

@login_required(login_url='/login')
def search_maintenance_requests(request):
    search_query = request.GET.get('search_query')

    maintenance_requests = MaintenanceRequest.objects.annotate(
        num_notes=Count('maintenance_notes')  # Count the number of maintenance notes for each request
    ).filter(
        Q(user_id__username__icontains=search_query) |
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(unit__icontains=search_query) |
        Q(building__building_name__icontains=search_query) |
        Q(status__icontains=search_query) |
        Q(priority__icontains=search_query) |
        Q(request__icontains=search_query) |
        Q(entry_permission__icontains=search_query) |
        Q(title__icontains=search_query) |
        Q(maintenance_notes__notes__icontains=search_query) |  # Search within maintenance notes
        Q(num_notes__gt=0)  # Filter requests with at least one maintenance note
    ).distinct()  # Ensure distinct results

    html_content = render_to_string('dashboard/data/requests.html', {'maintenance_requests': maintenance_requests})

    return JsonResponse({'html_content': html_content})

@login_required(login_url='/login')
def upload_image(request):
    if request.method == 'POST':
        print("ITS A POST REQUIRE")
        maintenance_request_id = request.POST.get('request_id')
        maintenance_request = get_object_or_404(MaintenanceRequest, pk=maintenance_request_id)
        images = request.FILES.getlist('images')
        for image in images:
            MaintenanceFile.objects.create(maintenanceRequestId=maintenance_request, file=image)
        return redirect('request_info', request_id=maintenance_request_id)
    else:
        return handler_500(request)


@login_required(login_url='/login')
def remove_image(request, image_id):
    if request.method == 'DELETE':
        try:
            maintenance_file = MaintenanceFile.objects.get(pk=image_id)
            maintenance_file.file.delete()
            maintenance_file.delete()
            return JsonResponse({'success': True})
        except MaintenanceFile.DoesNotExist:
            pass
    return JsonResponse({'success': False})


# Views for errors
def handler_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def handler_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def handler_500(request):
    return render(request, 'errors/500.html', status=500)