from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Fund(models.Model):
    class Meta:
        permissions = (
            ("apply_only", "可以提交申请"),
            ("student_approve", "学代通道"),
            ("teacher_approve", "老师通道"),
        )
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    apply_date = models.DateTimeField('申请日期', default=timezone.now)
    activity_date = models.DateField('活动日期', default=timezone.now)#, default=timezone.now
    plan_file = models.FileField(upload_to='%y/%m/%d/plan_file')
    charger = models.CharField(max_length=20)
    charger_tel = models.CharField(max_length=30)
    activity_member = models.CharField(max_length=500)
    last_time = models.CharField(max_length=100)
    note = models.CharField(max_length=500)
    is_viewed_by_student = models.BooleanField(default=False)
    is_viewed_by_teacher = models.BooleanField(default=False)
    is_objected = models.BooleanField(default=False)
    paycheck_file = models.FileField(upload_to='%y/%m/%d/paycheck_file',blank = True)
    pc_stat = {
            "not_uploaded": "等待提交结算表",
            "applied": "已提交结算表,等待审核",
            "stucon_approved": "学代已审核结算表",
            "stucon_disapproved": "结算表未通过学代审核",
            "teacher_approved": "老师已审核结算表",
            "teacher_disapproved": "结算表未通过老师审核",
    }
    paycheck_status = models.CharField(max_length=30,choices=tuple(pc_stat.keys()),default="not_uploaded")

    def __str__(self):
        return self.name

    def fund_status(self):
        if not self.is_objected:
            if self.is_viewed_by_student:
                if self.is_viewed_by_teacher:
                    return u"申请成功"
                else:
                    return u"等待老师审批"
            else:
                return u"等待学代审批"
        else:
            if self.is_viewed_by_student:
                if self.is_viewed_by_teacher:
                    return u"团委书记否决"
                else:
                    return u"学代否决"
'''
    def paycheck_to_display(self):
        if self.paycheck_status != "not_uploaded":
            return True
        else:
            return False
'''
