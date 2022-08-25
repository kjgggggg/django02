from django.db import models

# Create your models here.
class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11,null=True,)
    price = models.IntegerField(verbose_name="价格", null=True)

    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)

class Admin(models.Model):
    """管理员表"""
    adminName = models.CharField(verbose_name="管理员姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)