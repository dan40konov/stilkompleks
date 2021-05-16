from django.shortcuts import render, redirect
from .models import AddAccount
from .forms import AddAccountForm
from cryptography.fernet import Fernet
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
# Create your views here.


# def enc_dec():
#     key = Fernet.generate_key()
#     f = Fernet(key)
#     return f

def accounts_list(request):
    accounts_list = AddAccount.objects.all()

    context = {'accounts_list': accounts_list}
    return render(request, 'accounts_list.html', context)

def add_account(request):
    form = AddAccountForm

    if request.method == 'POST':
        form = AddAccountForm(request.POST)


        if form.is_valid():
            acc_pass1 = form.cleaned_data.get('password')
            acc_pass2 = form.cleaned_data.get('confirm_password')

            key = Fernet.generate_key()
            f = Fernet(key)
            enc_pass1 = f.encrypt(str.encode(acc_pass1))
            enc_pass2 = f.encrypt(str.encode(acc_pass2))
            pass_dec = f.decrypt(enc_pass1)


            print(pass_dec)

            account = form.save(commit=False)
            account.user = request.user
            account.password = enc_pass1.decode('utf-8')
            account.confirm_password = enc_pass2.decode('utf-8')
            account.enc_key = key.decode('utf-8')
            account.save()


            return render(request, 'dashboard.html')
        else:
            messages.error(request, "Both passwords didn't match")
            return redirect('add_account')

    return render(request, 'add_account.html', {'form': form})

def view_pass(request, pk):
    # try:
    #     global pk
    #     pk = request.GET['pk']
    #     #acc_pass = AddAccount.objects.filter('password')
    # except MultiValueDictKeyError:
    #     pk = False
    # id = AddAccount.objects.only(pk=pk).get(password=password).id

    #pass_dec = val()

    # qs = AddAccount.objects.get(pk=pk)
    # password = qs.password
    # print(password)

    #val = enc_dec()
    # key = Fernet.generate_key()
    # f = Fernet(key)
    #dec_pass = val.decrypt(password)

    #pass_dec = request.session['pass_dec']

    qs = AddAccount.objects.get(pk=pk)
    key = qs.enc_key.encode('utf-8')
    f = Fernet(key)
    dec_pass = f.decrypt(qs.password.encode('utf-8'))

    return render(request, 'view_pass.html', {'dec_pass':dec_pass.decode("utf-8")})


def update(request, pk):

    item = AddAccount.objects.get(pk=pk)
    form = AddAccountForm(request.POST or None, instance=item)

    if request.method == "POST":
        form = AddAccountForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            return redirect('account_list')
        else:
            return redirect('home')
    return render(request, 'update.html', {'item': item, 'form':form})


def delete(request, pk):
    item = AddAccount.objects.get(pk=pk)
    item.delete()
    return redirect('accounts_list')