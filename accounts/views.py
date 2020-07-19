from django.shortcuts import render,redirect
from django.http import  HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.tokens import default_token_generator

from .forms import *
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy

# Create your views here.

@unauthenticated_user
def registerPage(request):

    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request,'Account was created for'+ username)
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)
@unauthenticated_user
def loginPage(request):
   if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username and Password is incorrect.')
                context = {}
                return render(request, 'accounts/login.html', context)
   context={}
   return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()

    total_customers=customers.count()
    total_order = orders.count()
    delivered=orders.filter(status='Delivered').count
    pending=orders.filter(status='pending').count
    context={'orders':orders,'customers':customers,'total_customers':total_customers,'total_order': total_order,'delivered': delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def UserPage(request):
    orders=request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending= orders.filter(status='out for delivery').count()


    context = {'orders': orders,'delivered':delivered, 'pending': pending,'total_order':total_order }
    return render(request, 'accounts/user.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSetting(request):
    customer=request.user.customer
    form = CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'accounts/account_setting.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product=Product.objects.all()
    return render(request,'accounts/products.html',{'Product':product})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    order_count=orders.count()
    myfilters=OrderFilter(request.GET,queryset=orders)
    orders=myfilters.qs


    context={'customer':customer,'orders': orders,'order_count':order_count,'myfilters': myfilters}
    return render(request,'accounts/custmer.html',context)
def main(request):
    return render(request,'accounts/main.html')
def status(request):
    return render(request,'accounts/status.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    orderFormSet=inlineformset_factory(Customer, Order, fields=('product','status'), extra=10)
    customer=Customer.objects.get(id=pk)
    formset=orderFormSet(queryset=Order.objects.none(),instance=customer)
    # form=OrderForm(initial={'customer': customer})
    if request.method == "POST":
        #print("print Post",request.POST)
        # form=OrderForm(request.POST)
        formset=orderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form= OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context={'item':order}
    return render(request,'accounts/delete.html',context)


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = ('Password reset')
    token_generator = default_token_generator

