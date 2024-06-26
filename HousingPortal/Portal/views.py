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

def support_email(recipient, name, user_email, req):
    sender_email = "cs423robot@gmail.com" 
    recipient_email = recipient
    today = str(date.today())
    
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "Support Request"


    # write the text/plain part
    text = """\
    Hello, a support request has been made """ + today + "\n" +"""
    By: """ + name + "\temail: " + user_email + "\n" + """ 
    Message: """ + req
  

    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    #part2 = MIMEText(html, "html")
    message.attach(part1)
    #message.attach(part2)       


    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, "tjcm gvmf ilvq jnqy") 
        server.sendmail(sender_email, recipient_email, message.as_string())


def html_email(maintenance_request, recipient, subject, images=None):
    sender_email = "cs423robot@gmail.com" 
    recipient_email = recipient
    #subject = "Maintenance Request"
    dashboard = "https://tanrtech.com/dashboard/"
    today = str(date.today())
    
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    if(maintenance_request.entry_permission):
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
    Building: """ + maintenance_request.building.building_name + """
    Unit: """ + maintenance_request.unit + """
    Resident Name: """ + maintenance_request.first_name + " " + maintenance_request.last_name + """
    Phone: """ + maintenance_request.phone + """
    Request:""" + maintenance_request.request + """
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
    <td><strong>""" + maintenance_request.building.building_name + """</strong></td>
  </tr>
  <tr>
    <td>Unit:</td>
    <td><strong>""" + maintenance_request.unit + """</strong></td>
  </tr>
  <tr>
    <td>Resident Name:</td>
    <td><strong>""" + maintenance_request.first_name + " " + maintenance_request.last_name + """</strong></td>
  </tr>
  <tr>
    <td>Phone:</td>
    <td><strong>""" + maintenance_request.phone + """</strong></td>
  </tr>
  <tr>
    <td width:50px>Can we enter without<br> a resident present:</td>
    <td><strong>""" + enter + """</strong></td>
  </tr>
  <tr>
    <td>Title:</td>
    <td><strong>""" + maintenance_request.title + """</strong></td>
  </tr>
  <tr>
    <td>Request:</td>
    <td><strong>""" + maintenance_request.request + """</strong></td>
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

def send_email_thread(maintenance_request, recipient_email, subject, images):
    email_thread = threading.Thread(target=html_email, args=(maintenance_request, recipient_email, subject, images))
    email_thread.start()
    
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'home.html')

def support(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        name = first_name +" "+ last_name
        req = request.POST.get('request')

        support_email("cs423robot@gmail.com" , name, request.user.email, req)

        users_with_notifications = UserAccount.objects.filter(email_notifications=True)
        for user in users_with_notifications:
            if (user.is_superuser or user.is_manager) and user != request.user:
                support_email(user.email, name, request.user.email, req)


    return render(request, 'support.html')

@login_required(login_url="/login")
def dashboard(request):
    if request.user.is_superuser:
        users = UserAccount.objects.all().order_by('-id')[:10]
        maintenance_requests = MaintenanceRequest.objects.order_by('-id')[:10]
        buildings = Building.objects.all().order_by("id")
        return render(request, 'dashboard/admin_dashboard.html', {'users': users, 'maintenance_requests': maintenance_requests, 'buildings': buildings})
    elif request.user.is_manager:
        users = UserAccount.objects.all().order_by('-id')[:10]
        maintenance_requests = MaintenanceRequest.objects.order_by('-id')[:10]
        buildings = Building.objects.all().order_by("id")
        return render(request, 'dashboard/manager_dashboard.html', {'users':users, 'maintenance_requests':maintenance_requests, 'buildings': buildings})
    else:
        maintenance_requests = MaintenanceRequest.objects.filter(user_id=request.user.id).order_by("id")
        return render(request, 'dashboard/tenant_dashboard.html', {'maintenance_requests':maintenance_requests})

@login_required(login_url="/login")
def users(request):
    if request.user.is_superuser or request.user.is_manager:
        if request.headers.get('HX-Request'):
            search_query = request.GET.get('search_query')
            if search_query:
                users = UserAccount.objects.filter(
                    Q(username__icontains=search_query) |
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query) |
                    Q(email__icontains=search_query) |
                    Q(account_type__icontains=search_query)
                ).order_by(request.user.user_sort)
            else:
                users = UserAccount.objects.all().order_by(request.user.user_sort)

            paginator = Paginator(users, request.user.paging_count)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            html = render_to_string('dashboard/data/users_htmx.html', {'users': page_obj, 'user': request.user, 'total': users.count()})
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/users.html')
    else:
        return handler_403(request)

@login_required(login_url="/login")
def buildings(request):
    if request.user.is_superuser or request.user.is_manager:
        if request.headers.get('HX-Request'):
            search_query = request.GET.get('search_query')
            if search_query:
                buildings = Building.objects.filter(
                    Q(building_name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(city__icontains=search_query) |
                    Q(state__icontains=search_query) |
                    Q(country__icontains=search_query) |
                    Q(zipcode__icontains=search_query)
                ).order_by(request.user.building_sort)
            else:
                buildings = Building.objects.all().order_by(request.user.building_sort)

            paginator = Paginator(buildings, request.user.paging_count)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            html = render_to_string('dashboard/data/buildings_htmx.html', {'buildings': page_obj, 'user': request.user, 'total': buildings.count()})
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/buildings.html')
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def maintenance_requests(request):
    if request.user.is_superuser or request.user.is_manager:
        if request.headers.get('HX-Request'):
            search_query = request.GET.get('search_query')
            show_closed = request.GET.get('show_closed')
            if show_closed == 'true':
                # Show closed requests along with open requests
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
                    ).order_by(request.user.request_sort)
                else:
                    maintenance_requests = MaintenanceRequest.objects.all().order_by(request.user.request_sort)
            else:
                # Show only open requests
                if search_query:
                    maintenance_requests = MaintenanceRequest.objects.filter(
                        Q(status__in=['New', 'In Progress', 'Pending']) &
                        (
                            Q(id__icontains=search_query) |
                            Q(first_name__icontains=search_query) |
                            Q(last_name__icontains=search_query) |
                            Q(title__icontains=search_query) |
                            Q(status__icontains=search_query) |
                            Q(building__building_name__icontains=search_query) |
                            Q(unit__icontains=search_query) |
                            Q(entry_permission__icontains=search_query)
                        )
                    ).order_by(request.user.request_sort)
                else:
                    maintenance_requests = MaintenanceRequest.objects.filter(
                        status__in=['New', 'In Progress', 'Pending']
                    ).order_by(request.user.request_sort)

            paginator = Paginator(maintenance_requests, request.user.paging_count)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            html = render_to_string('dashboard/data/requests_htmx.html', {'request': request, 'maintenance_requests': page_obj, 'user': request.user, 'total': maintenance_requests.count()})
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/pages/maintenance_requests.html')
    else:
        return handler_403(request)
    
@login_required(login_url="/login")
def saved_requests(request):
    if request.headers.get('HX-Request'):
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
            ).order_by(request.user.request_sort)
        else:
            maintenance_requests = MaintenanceRequest.objects.filter(
                useraccountmaintenancerequest__user_id=request.user
            ).order_by(request.user.request_sort)

        paginator = Paginator(maintenance_requests, request.user.paging_count)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': page_obj, 'user': request.user, 'total': maintenance_requests.count()})
        return HttpResponse(html)
    else:
        return render(request, 'dashboard/pages/saved_requests.html')

@login_required(login_url="/login")
def maintenance(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
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

        maintenance_request = MaintenanceRequest.objects.create(user_id=request.user, first_name=first_name,
                                                               last_name=last_name, unit=unit, request=req, phone=phone,
                                                               building=building, priority=priority,
                                                               entry_permission=entry_permission, title=title,
                                                               date_submitted=date_submitted)

        image_paths = []

        for image in images:
            maintenance_file = MaintenanceFile.objects.create(maintenanceRequestId=maintenance_request, file=image)
            image_paths.append(maintenance_file.file.path)

        send_email_thread(maintenance_request,"cs423robot@gmail.com","Maintenance Request", image_paths)
        send_email_thread(maintenance_request, request.user.email,"Maintenance Request Confirmation", image_paths)

        # Send to users with email notifications on
        users_with_notifications = UserAccount.objects.filter(email_notifications=True)
        for user in users_with_notifications:
            if (user.is_superuser or user.is_manager) and user != request.user:
                send_email_thread(maintenance_request, user.email,"Maintenance Request Notification", image_paths)

        return redirect('/dashboard/requests/' + str(maintenance_request.id))
    
    buildings = Building.objects.all().order_by("building_name")
    return render(request, 'dashboard/create/maintenance.html', {'buildings': buildings})

@login_required(login_url="/login")
def building_info(request, building_id):
    if request.user.is_superuser or request.user.is_manager:
        building = get_object_or_404(Building, pk=building_id)
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
        elif request.headers.get('HX-Request'):
            maintenance_requests = MaintenanceRequest.objects.filter(building=building).order_by(request.user.request_sort)

            paginator = Paginator(maintenance_requests, request.user.paging_count)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': page_obj, 'user': request.user, 'total': maintenance_requests.count()})
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/info/building_info.html', {'building': building})
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


@login_required(login_url="/login")
def request_info(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    maintenance_files = MaintenanceFile.objects.filter(maintenanceRequestId=maintenance_request)
    if request.user.is_superuser or request.user.is_manager:
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

        buildings = Building.objects.all().order_by("building_name")
        maintenance_notes = maintenance_request.maintenance_notes.all()
        saved = request_is_saved(request, request_id)
        return render(request, 'dashboard/info/request_info.html', 
                      {'maintenance_request': maintenance_request, 'maintenance_files': maintenance_files, 'buildings': buildings, 'maintenance_notes': maintenance_notes, 'saved': saved})
    elif request.user == maintenance_request.user_id:
        maintenance_notes = maintenance_request.maintenance_notes.filter(tenant_viewable=True)
        saved = request_is_saved(request, request_id)
        return render(request, 'dashboard/info/request_info.html',
                      {'maintenance_request': maintenance_request, 'maintenance_files': maintenance_files,'maintenance_notes': maintenance_notes, 'saved': saved})
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
                    print(e.message_dict)
                    # Handle the validation error, e.g., return an error response
                    return JsonResponse({'errors': e.message_dict}, status=400)
            else:
                return JsonResponse({'errors': 'Not authorized'}, status=403)
        elif request.headers.get('HX-Request'):
            maintenance_requests = MaintenanceRequest.objects.filter(user_id=u).order_by(request.user.request_sort)

            paginator = Paginator(maintenance_requests, request.user.paging_count)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            html = render_to_string('dashboard/data/requests_htmx.html', {'maintenance_requests': page_obj, 'user': request.user, 'total': maintenance_requests.count()})
            return HttpResponse(html)
        else:
            return render(request, 'dashboard/info/user_info.html', {'u': u})
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
def create_building(request):
    user = request.user
    if user.is_superuser:
        form = BuildingForm()
        if request.method == 'POST':
            form = BuildingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/buildings')
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
        if (request.user.is_superuser or request.user.is_manager or request.user == maintenance_request.user_id):
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
    
@login_required(login_url="/login")
def change_preferences(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request_sort = data.get('request_sort')
        building_sort = data.get('building_sort')
        user_sort = data.get('user_sort')
        paging_count = data.get('paging_count')

        if request_sort:
            request.user.request_sort = request_sort
        if building_sort:
            request.user.building_sort = building_sort
        if user_sort:
            request.user.user_sort = user_sort
        if paging_count:
            request.user.paging_count = paging_count

        try:
            request.user.full_clean()  # This will run all validators on the model fields
            request.user.save()
            return JsonResponse({'success': True})
        except ValidationError as e:
            # Handle the validation error, e.g., return an error response
            return JsonResponse({'errors': e.message_dict}, status=400)
    


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

                    maintenance_files = MaintenanceFile.objects.filter(maintenanceRequestId=request)

                    for file in maintenance_files:
                        file.file.delete()
                        file.delete()

                    request.delete()

                    return JsonResponse({'success': True})
                except MaintenanceRequest.DoesNotExist:
                    return JsonResponse({'success': False})
                
        elif type == "MaintenanceNotes":
            if request.user.is_superuser or request.user.is_manager:
                try:
                    request_note = MaintenanceNotes.objects.get(pk=id_num)
                    request_note.delete()
                    return JsonResponse({'success': True})
                except MaintenanceNotes.DoesNotExist:
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
    if request.user.is_superuser or request.user.is_manager:
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