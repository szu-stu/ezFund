from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<fund_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<fund_id>[0-9]+)/approve', views.approve, name='approve'),
    url(r'^(?P<fund_id>[0-9]+)/deny', views.deny, name='deny'),
    url(r'^(?P<fund_id>[0-9]+)/upload_paycheck', views.upload_paycheck, name='paycheck_upload'),
    url(r'^(?P<fund_id>[0-9]+)/paycheck_approve', views.paycheck_approve, name='paycheck_approve'),
    url(r'^(?P<fund_id>[0-9]+)/paycheck_deny', views.paycheck_deny, name='paycheck_deny'),
    url(r'^apply/$', views.apply, name='apply'), 
]
