from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from .forms import SignUpForm, ProductCreateForm
from django.contrib.auth import login
from .models import Product, Order, Return, User
from django.contrib import messages


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/base.html', {'user': request.user})


class LoginPage(LoginView):
    template_name = 'shop/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
        context['form'].fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        return context


class LogoutPage(LogoutView):
    next_page = reverse_lazy('home')


class SignupPage(CreateView):
    form_class = SignUpForm
    template_name = 'shop/signup.html'

    def form_valid(self, form):
        self.object = form.save()

        login(self.request, self.object)
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
        context['form'].fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Password (Again)'
        })
        return context


# BASKET PAGE(USER)
class PurchasePage(ListView):
    model = Order
    template_name = 'shop/user_purchases.html'
    paginate_by = 15

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# MAKE A PURCHASE(HOME)
class ProductPurchase(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = Order
    fields = ['count']

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        product_pk = self.kwargs['pk']
        product = Product.objects.get(pk=product_pk)
        count = form.cleaned_data['count']
        user = self.request.user
        wallet = User.objects.filter(username=self.request.user.username).values('wallet').first()['wallet']

        if product.count < count:
            messages.error(self.request, f'There`s not enough count product! Only {product.count} of it is available')
            return redirect('home')

        total_price = count * product.price
        if total_price > wallet:
            messages.error(self.request, f'You don`t have enough money!')
            return redirect('home')

        self.object = form.save(commit=False)
        self.object.user = user
        self.object.product = product
        self.object.save()

        product.count -= count
        product.save()

        wallet -= total_price
        User.objects.filter(username=self.request.user.username).update(wallet=wallet)
        messages.success(self.request, f'The purchase was successfully completed!')
        return super().form_valid(form=form)


# HOME PAGE
class ProductPage(ListView):
    model = Product
    template_name = 'shop/home.html'
    extra_context = {'purchase_form': ProductPurchase()}
    paginate_by = 10


# CREATE PAGE(ADMIN)
class ProductCreatePage(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'shop/create_products.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Product Name'
        })
        context['form'].fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })
        context['form'].fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Price'
        })
        context['form'].fields['count'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Count'
        })
        return context


# UPDATE PAGE(ADMIN)
class ProductUpdatePage(UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'shop/update_products.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')


# RETURN PAGE(ADMIN)
class ReturnAdminPage(ListView):
    model = Return
    template_name = 'shop/return_page.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class CreateReturnPage(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = Return
    fields = []

    def get_success_url(self):
        return reverse_lazy('user_purchase')

    def form_valid(self, form):
        order_pk = self.kwargs['pk']
        order = Order.objects.get(pk=order_pk)

        if (timezone.now() - order.datatime_of_purchase).seconds > 180:
            messages.error(self.request, f'The time is expired, 3 minutes have passed since the purchase')
            return redirect('user_purchase')

        self.object = form.save(commit=False)
        self.object.order = order
        self.object.save()

        return super().form_valid(form=form)


class AcceptReturnAdmin(DeleteView):
    model = Return

    def form_valid(self, form):
        return_pk = self.kwargs['pk']
        return_form = Return.objects.get(pk=return_pk)
        order = return_form.order

        product = order.product
        user = order.user

        wallet = User.objects.filter(username=user.username).values('wallet').first()['wallet']

        product.count += order.count
        wallet += product.price * order.count
        User.objects.filter(username=user.username).update(wallet=wallet)
        product.save()

        return_form.delete()
        order.delete()

        return redirect('return_product')


class RefuseReturnAdmin(DeleteView):
    model = Return

    def get_success_url(self):
        return reverse_lazy('return_product')

    def form_valid(self, form):
        return_pk = self.kwargs['pk']
        return_form = Return.objects.get(pk=return_pk)

        return_form.delete()

        return redirect('return_product')