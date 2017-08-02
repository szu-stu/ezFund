from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Fund

from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from operator import itemgetter, attrgetter

from .forms import FundForm, UserForm
from .check_per import detial_cp_decorator, apply_cp_decorator

from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group



@login_required(login_url='/login/')
def index(request):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        student_view = False
        stucon_view = True
        fund_objects = Fund.objects.all()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            student_view = False
            stucon_view = False
            fund_objects = (Fund.objects.filter(is_objected=False, is_viewed_by_student=True) | Fund.objects.filter( is_viewed_by_teacher=True))
        else:
            if now_user.has_perm(perm="fund.apply_only"):
                student_view = True
                stucon_view = False
                fund_objects = Fund.objects.filter(username = now_user.username)
    fund_list = sorted(fund_objects, key=attrgetter('id'), reverse=True)
    paginator = Paginator(fund_list,10)
    page = request.GET.get('page')
    try:
        fund_list = paginator.page(page)
    except PageNotAnInteger:
        fund_list = paginator.page(1)
    except EmptyPage:
        fund_list = paginator.page(paginator.num_pages)
    context = {
        'student_view': student_view,
        'stucon_view': stucon_view,
        'username': request.user.username,
        'fund_list': fund_list,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
@detial_cp_decorator
def detail(request, fund_id):
    now_user = request.user
    fund = get_object_or_404(Fund, pk=fund_id)
    if request.user.has_perm(perm="fund.apply_only"):
        work_btn = False
    else:
        work_btn = True
    if now_user.has_perm(perm="fund.student_approve"):
        stucon_view = True
    else:
        stucon_view = False
    content = {
        'username': request.user.username,
        'fund': fund,
        'fund_stat': fund.fund_status(),
        'show_work_btn': work_btn,
        'stucon_view': stucon_view,
    }
    return render(request, 'detail.html', content)


@login_required(login_url='/login/')
@apply_cp_decorator
def apply(request):
    now_user = request.user
    if request.method == 'POST':
        form = FundForm(request.POST, request.FILES)
        if form.is_valid():
            apply_object = form.save()
            apply_object.username = now_user.username
            apply_object.save()
            success = True
            return render(request, 'apply.html', {'success':success})
        else:
            error = form.errors
            form = FundForm
            context = {
                'error':error,
                'form':form,
            }
            return render(request, 'apply.html', context)
    else:
        form = FundForm
    return render(request, 'apply.html', {'form':form})


@login_required(login_url='/login/')
def approve(request, fund_id):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_viewed_by_student = True
        app_fund.save()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_viewed_by_teacher = True
            app_fund.save()
    return detail(request, fund_id)


@login_required(login_url='/login/')
def deny(request, fund_id):
    now_user = request.user
    if now_user.has_perm(perm="fund.student_approve"):
        app_fund = get_object_or_404(Fund, pk=fund_id)
        app_fund.is_viewed_by_student = True
        app_fund.is_objected = True
        app_fund.save()
    else:
        if now_user.has_perm(perm="fund.teacher_approve"):
            app_fund = get_object_or_404(Fund, pk=fund_id)
            app_fund.is_viewed_by_teacher = True
            app_fund.is_objected = True
            app_fund.save()
    return detail(request, fund_id)

#未来添加双重密码验证注册
def SignUpView(request):
    if request.method == "POST":
        SignUpForm = UserForm(request.POST)
        if SignUpForm.is_valid():
            username = SignUpForm.cleaned_data['username']
            password = SignUpForm.cleaned_data['password']
            email = SignUpForm.cleaned_data['email']
            if User.objects.filter(username=username):
                SignUpForm = UserForm
                context = {
                    'SignUpForm': SignUpForm,
                    'reason': '用户名已存在，请选择其他用户名',
                    'username': request.user.username,
                    }
                return render(request, 'account/sign_up.html',context)
            else:
                user = User.objects.create_user(username, email, password)
                user.is_staff = True
                default_group = Group.objects.get(name='student union')
                default_group.user_set.add(user)
                user.save()
                login(request, authenticate(username=username, password=password))
                return HttpResponseRedirect('/')
        else:
            error = SignUpForm.errors
            SignUpForm = UserForm
            context = {
                'SignUpForm': SignUpForm,
                'reason': error,
                'username': request.user.username,
                }
            return render(request, 'account/sign_up.html', context)
    else:
        SignUpForm = UserForm
        context = {
            'SignUpForm': SignUpForm,
            'username': request.user.username,
        }
        return render(request, 'account/sign_up.html', context)

 
def logoutnlogin(request):
    """
    Logout n login back
    """
    return auth_views.logout_then_login(request,login_url='/login')







