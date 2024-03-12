from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import login, authenticate
def main(request):
    return render(request,'main.html')

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
# views.py
from django.contrib.auth.forms import UserCreationForm
from .forms import UserDeleteForm, ProductForm, ProductDeleteForm, UserAddForm

def user_monitoring(request):
    if not request.user.is_superuser:
        # Redirect non-admin users
        return redirect('home')  # Replace 'home' with your desired URL

    registered_users = User.objects.all()

    active_sessions = []
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in all_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            active_sessions.append({
                'username': user.username,
                'last_activity': session.expire_date
            })

    products = Product.objects.all()
    user_delete_form = UserDeleteForm()
    user_add_form = UserAddForm()
    product_form = ProductForm()
    product_delete_form = ProductDeleteForm()

    context = {
        'registered_users': registered_users,
        'active_sessions': active_sessions,
        'products': products,
        'user_delete_form': user_delete_form,
        'user_add_form': user_add_form,
        'product_form': product_form,
        'product_delete_form': product_delete_form,
    }
    return render(request, 'admin.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import Product
from .forms import UserDeleteForm, ProductForm, ProductDeleteForm, UserAddForm

def user_monitoring(request):
    if not request.user.is_superuser:
        # Redirect non-admin users to the login page
        return redirect('login')

    registered_users = User.objects.all()

    active_sessions = []
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in all_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            active_sessions.append({
                'username': user.username,
                'last_activity': session.expire_date
            })

    products = Product.objects.all()

    # Handle form submissions
    user_delete_form = UserDeleteForm()
    user_add_form = UserAddForm()
    product_form = ProductForm()
    product_delete_form = ProductDeleteForm()

    context = {
        'registered_users': registered_users,
        'active_sessions': active_sessions,
        'products': products,
        'user_delete_form': user_delete_form,
        'user_add_form': user_add_form,
        'product_form': product_form,
        'product_delete_form': product_delete_form,
    }
    return render(request, 'admin.html', context)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_monitoring')
from django.shortcuts import redirect, get_object_or_404
from .models import Product

def delete_product(request, product_id):
    # Retrieve the product object or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the product object
        product.delete()
        # Redirect to the user monitoring page after deletion
        return redirect('user_monitoring')
    else:
        # If the request method is not POST, handle it accordingly (e.g., return an error response)
        pass
# views.py
from django.shortcuts import render, redirect
from .forms import UserAddForm

def add_user(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_monitoring')  # Redirect to the user monitoring page after adding the user
    else:
        form = UserAddForm()
    
    context = {
        'user_add_form': form,
    }
    return render(request, 'admin.html', context)
from django.shortcuts import render, redirect
from .forms import ProductForm

def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new product
            form.save()
            # Redirect to a success URL or render a success page
            return redirect('user_monitoring')  # Assuming 'user_monitoring' is the URL name for the user monitoring page
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'product_form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the user dashboard page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    page='user'
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the appropriate page after successful login
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form,'page':page})

@login_required(login_url='login')
def user_dashboard(request):
    users = User.objects.all()  # Assuming you have a User model
    products = Product.objects.all()
    return render(request, 'user_dashboard.html', {'users': users, 'products': products})

def admin_login(request):
    page='admin'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('user_monitoring')  # Redirect to admin dashboard or desired page upon successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form,'page':page})