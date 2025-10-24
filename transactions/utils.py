from django.shortcuts import redirect
from functools import wraps

def admin_decorators(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_admin')
        if request.user.role != "ADMIN":
            return redirect('login_admin')
        return view_func(request, *args, **kwargs)
    return wrapper