from django.shortcuts import render, redirect
from.models import Product
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def product(request):
    return render(request, 'pages/product.html')

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
