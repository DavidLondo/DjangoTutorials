from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages


class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: David Londoño Palacio",
        })
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Our contact methods",
            "description": "This is a Contact Page ...",
            "author": "Developed by: David Londoño Palacio",
            "email": "Onlinestore@gmail.com",
            "address": "4th Street, Washington D.C",
            "phone": "304212453"
        })
        return context
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": "400"},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": "1200"},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": "300"},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": "150"}
    ]
class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            id = int(id)
            if id < 1 or id > len(Product.products):
                return HttpResponseRedirect(reverse("home"))
            product = Product.products[id - 1]
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse("home"))

        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        viewData["price"] = "$" + product["price"]

        return render(request, self.template_name, viewData)
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise forms.ValidationError("The price must be greater than zero.")
        return price
    
class ProductCreateView(View):
    template_name = 'products/create.html'
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            messages.success(request, "Product created successfully")
            return redirect('form')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
        return render(request, self.template_name, viewData)