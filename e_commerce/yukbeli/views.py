from django.shortcuts import render
from .models import Product, OrderItem, Customer, Order, ShippingAddress
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from django.contrib.auth.models import User

# Create your views here.

def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
         items = []
         order = {"get_cart_items":0, "get_cart_total":0}
    context = {"items":items, "order":order, "products":products}
    return render(request, "yukbeli/home.html", context)

@login_required()
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items":0, "get_cart_total":0}
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        if product_id and quantity >= 0:
            order_item = order.orderitem_set.get(product_id=product_id)
            order_item.quantity = quantity
            order_item.save()

    context = {"items": items, "order": order}
    context = {"items":items, "order":order}
    return render(request, 'yukbeli/cart.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity += 1
            order_item.save()
            return redirect('home')

    # If not authenticated or any other error, redirect to home or handle accordingly
    return redirect('home')

@login_required()  # Add login_required decorator
def logout_request(request):
    logout(request)
    return redirect('home')   

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        existing_customers = Customer.objects.filter(email=email)

        if existing_customers.exists():
            form.add_error('email', 'Email is already taken')
            return self.render_to_response(self.get_context_data(form=form))

        response = super().form_valid(form)
        customer = Customer.objects.create(user=self.object, name=self.object.username, email=email)
        customer.save()

        return response
    
@login_required()
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}

    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # Save shipping address to the order
            address = form.cleaned_data.get("address")
            city = form.cleaned_data.get("city")
            state = form.cleaned_data.get("state")
            zipcode = form.cleaned_data.get("zipcode")
            shipping = ShippingAddress.objects.create(customer=customer, 
                                                      order=order,
                                                      address = address,
                                                      city=city,
                                                      zipcode=zipcode,
                                                      state=state)
            
            shipping.save()
            shipping_info = ShippingAddress.objects.get(pk=shipping.pk)
            context_form = {"form": form, "shipping" : shipping_info}
            return render(request, 'yukbeli/thanks.html', context=context_form)

    context = {"items": items, "order": order, "form": ShippingAddressForm()}  # Pass an instance of the form to the template

    return render(request, 'yukbeli/checkout.html', context)

