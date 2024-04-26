from django.shortcuts import render, redirect,get_object_or_404
from.models import Product ,CartItem
from django.db.models import Q
from .forms import CustomerForm,LoginForm,AuthenticationForm
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def product(request):
    return render(request, 'pages/product.html')

def contact(request):
    return render(request, 'pages/contact.html')

def product_page(request):
    products = Product.objects.all()
    return render(request, 'pages/product.html', {'products': products})


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
            form.save()
            return redirect('success')  
    else:
        form = CustomerForm()
    return render(request, 'pages/registration.html', {'form': form})
    
def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    context = {
        'cart_items': cart_items
    }
    return render(request, 'pages/cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
       
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=product_id)  
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('product_page')
    else:
        return redirect('login')
    

@login_required
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})