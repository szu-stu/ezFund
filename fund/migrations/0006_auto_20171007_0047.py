# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-06 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0005_auto_20170730_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='paycheck_file',
            field=models.FileField(blank=True, upload_to='%y/%m/%d/paycheck_file'),
        ),
        migrations.AddField(
            model_name='fund',
            name='paycheck_status',
            field=models.CharField(choices=[('not_uploaded', '等待提交结算表'), ('applied', '已提交结算表，等待审核'), ('stucon_approved', '学代已审核结算表'), ('stucon_disapproved', '结算表未通过学代审核'), ('teacher_approved', '老师已审核结算表'), ('teacher_disapproved', '结算表未通过老师审核')], default='not_uploaded', max_length=30),
        ),
    ]