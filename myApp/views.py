from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, CartItem, UserProfile, Contact
from .forms import CustomerForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed

def index(request):
    return render(request, 'pages/index.html')

def order(request):
    return render(request, 'pages/order.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == "POST":
        contact=Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        subject=request.POST.get('subject')
        contact.name=name
        contact.email=email
        contact.mobile=mobile
        contact.subject=subject
        contact.save()
        return HttpResponse("<h1> Thanks for contacting us </h1>")
    return render(request, 'pages/contact.html')

def product_page(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'pages/product.html', {'products': products})


def register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  
    else:
        form = CustomerForm()
    return render(request, 'pages/registration.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm(request)
    return render(request, 'pages/login.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'pages/profile.html', {'form': form, 'profile': profile})

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.product_ref.selling_price * item.quantity
    return render(request, 'pages/cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_ref=product) 
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('product_page')
    else:
        return redirect('login')


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
        messages.warning(request, 'Are you sure you want to remove this item from your cart?')
        cart_item.delete()
        return redirect('/cart')  
    else:
        return HttpResponseNotAllowed(['POST'])