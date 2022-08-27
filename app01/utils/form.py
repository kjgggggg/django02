from django.core.exceptions import ValidationError
from django import forms


from app01 import models
from django.core.validators import RegexValidator

from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


class PrettyModelForm(forms.ModelForm):

    # 验证方法1:
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误")]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["id", "mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    # 验证方法2 :钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        return txt_mobile


class PrettyModelForm1(forms.ModelForm):
    mobile = forms.CharField(disabled=True, label="手机号")
    # 验证方法1:

    class Meta:
        model = models.PrettyNum
        fields = ["id", "mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


class AdminModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["adminName", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("请输入相同密码")
        return confirm


class AdminModelForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = models.Admin
        fields = ["adminName"]


class AdminModelForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput,
            "confirm_password": forms.PasswordInput,
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的一致")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("请输入相同密码")
        return confirm


class AccountModelForm(BootStrapModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control"}
    code = forms.CharField(label="验证码")

    class Meta:
        model = models.Admin
        fields = ["adminName", "password", "code"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        return md5_pwd


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"  # 所有的字段


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        exclude = ["oid", "admin"]