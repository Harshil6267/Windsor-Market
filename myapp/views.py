from django.shortcuts import get_object_or_404
from .models import Category, Product, Client, Order
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, reverse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime


def index(request):
    if 'username' in request.session:
        cat_list = Category.objects.all().order_by('id')[:10]
        if 'last_login' in request.session:
            last_log = request.session.get('last_login')
        else:
            last_log = "Your last login was more than one hour ago"
        return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_log': last_log, 'user': request.session['username']})
    else:
        return redirect('/myapp/login/')


def about(request):
    if 'username' in request.session:
        cookie_value = request.COOKIES.get('about_visits', 'default')
        if cookie_value == 'default':
            response = render(request, 'myapp/about.html', {'about_visits': '1'})
            response.set_cookie('about_visits', 1, 5*60)
            return response
        else:
            cookie_value = int(cookie_value) + 1
            response = render(request, 'myapp/about.html', {'about_visits': cookie_value})
            response.set_cookie('about_visits', cookie_value)
            return response
    else:
        return redirect('/myapp/login/')


def detail(request, cat_no):
    # Category.objects.filter(id=cat_no).Product_set.all()
    cat_list = get_object_or_404(Category, id=cat_no)
    product_list = Product.objects.filter(category__id=cat_no)
    return render(request, 'myapp/detail.html', {'cat_list': cat_list,'product_list': product_list})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist':prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Order placed succesfully.'
            else:
                msg = 'We dont have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html' , {'msg':msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    product = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            data = form.data
            print('Interested:', data.get('interested'), data.get('quantity'))
            if data.get('interested') == '1':
                print('ProductInt', product.intrested)
                product.intrested = product.intrested + 1
            product.save()
        return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form':form, 'product':product})
    # return render(request, 'myapp/productdetail.html', {'product':product})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                current_login_time = str(datetime.datetime.now())
                request.session['last_login'] = current_login_time
                request.session.set_expiry(3600)
                request.session['username'] = username
                login(request, user)
                if 'after_login' in request.session:
                    return redirect('/myapp/myorders/')
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))

            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')

    else:
        return render(request, 'myapp/login.html')


def myorders(request):
    if request.session.has_key('username'):
        username = request.session['username']
        my_order_list = Order.objects.filter(client__username=username)
        return render(request, 'myapp/myorder.html', {'myorderlist': my_order_list})
    else:
        request.session['after_login'] = 'myorders'
        return redirect('/myapp/login/')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/myapp/products/')


def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            current_login_time = str(datetime.datetime.now())
            request.session['last_login'] = current_login_time
            request.session['username'] = username
            return redirect('/myapp/index/')
    else:
        form = Register()
    return render(request, 'myapp/register.html', {'form': form})


def profile(request):
    if request.session.has_key('username'):
       username = request.session['username']
       client_detail = Client.objects.filter(username=username)
       return render(request, 'myapp/profile.html', {'client_detail': client_detail})