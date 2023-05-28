from datetime import datetime
from traceback import print_tb
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from gsmsApp import models, forms
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required



def context_data():
    context = {
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Petrol Pump Management System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

@login_required
def upload_modal(request):
    context = context_data()
    return render(request, 'upload.html', context)


def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def update_profile(request):
    context = context_data()
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    context =context_data()
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['total_type'] = models.Petrol.objects.filter(delete_flag = 0, status = 1).count()
    context['petrols'] = models.Petrol.objects.filter(delete_flag = 0, status = 1).all()
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    try:
        petrols = models.Petrol.objects.filter(delete_flag = 0, status = 1).all().values_list('id')
        total_amount = models.Sale.objects.filter(petrol__id__in = petrols).aggregate(Sum('amount'))['amount__sum']
        if total_amount is None:
            total_amount = 0
    except:
        total_amount = 0

    context['total_sales'] =  total_amount

    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data()
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)


#Petrol Type
@login_required
def petrol_list(request):
    context =context_data()
    context['page_title'] = "Petrol Type List"
    context['page'] = "petrol_list"
    context['petrols'] = models.Petrol.objects.filter(delete_flag = 0).all()

    return render(request, "petrol_list.html", context)

@login_required
def manage_petrol(request,pk=None):
    context=context_data()
    context['petrol'] = {}
    if not pk is None:
        context['petrol'] = models.Petrol.objects.get(id=pk)
    
    return render(request,'manage_petrol.html', context)

@login_required
def view_petrol(request,pk=None):
    context=context_data()
    context['petrol'] = {}
    if not pk is None:
        context['petrol'] = models.Petrol.objects.get(id=pk)
    
    return render(request,'petrol_details.html', context)
        

@login_required
def save_petrol(request, pk = None):
    resp = {'status':'failed', 'msg':''}
    if not request.method =='POST':
        resp['msg'] = "No data send on this request"
    else:
        post = request.POST
        if not post['id'] == '':
            petrol = models.Petrol.objects.get(id = post['id'])
            form = forms.SavePetrol(request.POST, instance=petrol)
        else:
            form = forms.SavePetrol(request.POST)
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Petrol Type has been added successfully")
            else:
                messages.success(request, "Petrol Type has been updated successfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.label}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_petrol(request, pk = None):
    resp = {'status':'failed', 'msg':''}
    if pk is None:
        resp['msg'] = "Invalid Petrol Type ID"
    else:
        try:
            petrol = models.Petrol.objects.filter(id=pk).update(delete_flag = 1)
            resp['status'] = 'success'
            messages.success(request, "Petrol Type has been deleted successfully")
        except:
            resp['msg'] = "Invalid Petrol Type ID"

    return HttpResponse(json.dumps(resp), content_type="application/json")

#Stock Record
@login_required
def stock_list(request):
    context =context_data()
    context['page_title'] = "Stock Records"
    context['page'] = "stock_list"
    petrols = models.Petrol.objects.filter(delete_flag = 0, status = 1).all().values_list('id')
    context['stocks'] = models.Stock.objects.filter(petrol__id__in = petrols).all()

    return render(request, "stock_list.html", context)

@login_required
def manage_stock(request,pk=None):
    context=context_data()
    context['stock'] = {}
    if not pk is None:
        context['stock'] = models.Stock.objects .get(id=pk)
    context['petrols'] = models.Petrol.objects.filter(delete_flag = 0, status = 1).all()
    return render(request,'manage_stock.html', context)

@login_required
def view_stock(request,pk=None):
    context=context_data()
    context['stock'] = {}
    if not pk is None:
        context['stock'] = models.Stock.objects.get(id=pk)
    
    return render(request,'stock_details.html', context)
        

@login_required
def save_stock(request, pk = None):
    resp = {'status':'failed', 'msg':''}
    if not request.method =='POST':
        resp['msg'] = "No data send on this request"
    else:
        post = request.POST
        if not post['id'] == '':
            stock = models.Stock.objects.get(id = post['id'])
            form = forms.SaveStock(request.POST, instance=stock)
        else:
            form = forms.SaveStock(request.POST)
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Stock Record has been added successfully")
            else:
                messages.success(request, "Stock Record has been updated successfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.label}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_stock(request, pk = None):
    resp = {'status':'failed', 'msg':''}
    if pk is None:
        resp['msg'] = "Invalid Stock Record ID"
    else:
        try:
            stock = models.Stock.objects.filter(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, "Stock Record has been deleted successfully")
        except:
            resp['msg'] = "Invalid Stock Record ID"

    return HttpResponse(json.dumps(resp), content_type="application/json")
    

@login_required
def inventory(request):
    context =context_data()
    context['page_title'] = "Inventory"
    context['page'] = "inventory_page"
    context['petrols'] = models.Petrol.objects.filter(delete_flag = 0, status = 1).all()

    return render(request, "inventory.html", context)


#Sale Record
@login_required
def sale_list(request):
    context =context_data()
    context['page_title'] = "Sale Records"
    context['page'] = "sale_list"
    petrols = models.Petrol.objects.filter(delete_flag = 0, status = 1).all().values_list('id')
    context['sales'] = models.Sale.objects.filter(petrol__id__in = petrols).all()

    return render(request, "sale_list.html", context)

@login_required
def manage_sale(request,pk=None):
    context=context_data()
    context['sale'] = {}
    if not pk is None:
        context['sale'] = models.Sale.objects .get(id=pk)
    context['petrols'] = models.Petrol.objects.filter(delete_flag = 0, status = 1).all()
    return render(request,'manage_sale.html', context)

@login_required
def view_sale(request,pk=None):
    context=context_data()
    context['sale'] = {}
    if not pk is None:
        context['sale'] = models.Sale.objects.get(id=pk)
    
    return render(request,'sale_details.html', context)
        

@login_required
def save_sale(request, pk = None):
    resp = {'status':'failed', 'msg':''}
    if not request.method =='POST':
        resp['msg'] = "No data send on this request"
    else:
        post = request.POST
        if not post['id'] == '':
            sale = models.Sale.objects.get(id = post['id'])
            form = forms.SaveSale(request.POST, instance=sale)
        else:
            form = forms.SaveSale(request.POST)
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Sale Record has been added successfully")
            else:
                messages.success(request, "Sale Record has been updated successfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.label}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_sale(request, pk = None):
    resp = {'status':'failed', 'msg':''}
    if pk is None:
        resp['msg'] = "Invalid Sale Record ID"
    else:
        try:
            sale = models.Sale.objects.filter(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, "Sale Record has been deleted successfully")
        except:
            resp['msg'] = "Invalid Sale Record ID"

    return HttpResponse(json.dumps(resp), content_type="application/json")

#Sale Report
@login_required
def sales_report(request, rep_date=None):
    context =context_data()
    context['page_title'] = "Sale Report"
    context['page'] = "sale_list"
    if not rep_date is None:
        rep_date = datetime.strptime(rep_date, "%Y-%m-%d")
    else:
        rep_date = datetime.now()
    year = rep_date.strftime("%Y")
    month = rep_date.strftime("%m")
    day = rep_date.strftime("%d")
    petrols = models.Petrol.objects.filter(delete_flag = 0, status = 1).all().values_list('id')
    sales = models.Sale.objects.filter(petrol__id__in = petrols, 
                                                  date__month = month,
                                                  date__day = day,
                                                  date__year = year,
                                                  )
    context['rep_date'] = rep_date
    context['sales'] = sales.all()
    context['total_amount'] = sales.aggregate(Sum('amount'))['amount__sum']
    if context['total_amount'] is None:
        context['total_amount']= 0

    return render(request, "sales_report.html", context)