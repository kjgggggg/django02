from django.core.exceptions import ValidationError
from django.shortcuts import render,HttpResponse,redirect
from django import forms
# Create your views here.
from django.utils.safestring import mark_safe

from app01 import models
from django.core.validators import RegexValidator
from app01.utils.pagination import Pagination


def pretty_list(request):


    data_list = {}
    value = request.GET.get("q", "")  # " "为默认值

    if value:
        data_list["mobile__contains"] = value
    queryset = models.PrettyNum.objects.filter(**data_list).order_by("id")

    page_object = Pagination(request, queryset)

    return render(request, 'pretty_list.html', {"value": value, "queryset": page_object.page_queryset, "page_string": page_object.html()})





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