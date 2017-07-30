from django.shortcuts import get_object_or_404, render
from .models import Fund
from django.contrib.auth.models import User, Group

def detial_cp_decorator(function):
    def wrapped_check(request, fund_id, *args, **kwargs):
        now_user = request.user
        fund = get_object_or_404(Fund, pk=fund_id)
        try:
            now_group = Group.objects.get(user=now_user)
            if now_group.name == 'student union':
                if now_user.username != fund.username:
                    return render(request, 'deny.html', {'message':'不能查看他人详情页'})
            return function(request,fund_id, *args, **kwargs)
        except:
            return function(request,fund_id, *args, **kwargs)
    return wrapped_check

def apply_cp_decorator(function):
    def wrapped_check(request,*args, **kwargs):
        now_user = request.user
        if not now_user.has_perm(perm="fund.apply_only"):
            return render(request, 'deny.html', {'message':'不能查看他人详情页'})
        return function(request,*args, **kwargs)
    return wrapped_check