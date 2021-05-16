from django.shortcuts import redirect
from django.http import HttpResponse

def not_authenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return HttpResponse("You are not allowed to access this page")

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function



    