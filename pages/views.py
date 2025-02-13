from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise forms.ValidationError("The price must be greater than zero.")
        return price
    
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
    
class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": product.name + " - Online Store",
            "subtitle": product.name + " - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)

class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ Ahora funcionará correctamente
            messages.success(request, "Product created successfully")
            return redirect('index')  # Asegúrate de que esta URL existe
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
        return render(request, self.template_name, viewData)
