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

    def __str__(self):
        return self.adminName


class Task(models.Model):
    """ 任务表 """
    level_choice = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详情")
    admin = models.ForeignKey(verbose_name="负责人", to="Admin", to_field="id", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    # admin_id
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)