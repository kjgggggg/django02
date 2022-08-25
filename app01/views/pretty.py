from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from django import forms
# Create your views here.
from django.utils.safestring import mark_safe

from app01 import models
from django.core.validators import RegexValidator

from app01.utils.form import PrettyModelForm
from app01.utils.pagination import Pagination
from app01.utils.encrypt import md5


def pretty_list(request):

    data_list = {}
    value = request.GET.get("q", "")  # " "为默认值

    if value:
        data_list["mobile__contains"] = value
    queryset = models.PrettyNum.objects.filter(**data_list).order_by("id")

    page_object = Pagination(request, queryset)

    return render(request, 'pretty_list.html', {"value": value, "queryset": page_object.page_queryset, "page_string": page_object.html()})


def pretty_add(request):
    form = PrettyModelForm()
    if request.method == "GET":
        return render(request, 'pretty_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {"form": form})


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


def pretty_edit(request, nid):
    if request.method == "GET":
        obj = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyModelForm1(instance=obj)
        return render(request, 'pretty_edit.html', {"form": form})

    obj = models.PrettyNum.objects.filter(id=nid).first()
    form = PrettyModelForm1(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')


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
