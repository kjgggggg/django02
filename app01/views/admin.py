from django.core.exceptions import ValidationError
from django.shortcuts import render,HttpResponse,redirect
from django import forms
# Create your views here.
from django.utils.safestring import mark_safe

from app01 import models
from django.core.validators import RegexValidator

from app01.utils.form import AdminModelForm2, AdminModelForm1, AdminModelForm
from app01.utils.pagination import Pagination
from app01.utils.encrypt import md5

def admin_list(request):

    # info_dict = request.session["info"]

    data_list = {}
    value = request.GET.get("q", "")  # " "为默认值

    if value:
        data_list["adminName__contains"] = value
    queryset = models.Admin.objects.filter(**data_list).order_by("id")

    page_object = Pagination(request, queryset)

    return render(request, 'admin_list.html', {"value": value, "queryset": page_object.page_queryset, "page_string": page_object.html()})


def admin_add(request):
    form = AdminModelForm()
    if request.method == "GET":
        return render(request, 'admin_add.html', {"form": form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 能获取到已经经过验证的form信息 {'adminName':'a', 'password':'123', 'confirm_password':'333'}
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_add.html', {"form": form})


def admin_edit(request, nid):
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect('/admin/list/')
    if request.method == "GET":
        form = AdminModelForm1(instance=obj)
        return render(request, 'admin_edit.html', {"form": form})

    form = AdminModelForm1(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_edit.html', {"form": form})


def admin_delete(request, nid):
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect('/admin/list/')
    models.Admin.objects.filter(id=nid).first().delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """ 重置密码  """
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect('/admin/list/')

    if request.method == "GET":
        form = AdminModelForm2()
        return render(request, 'admin_reset.html', {"form": form})
    form = AdminModelForm2(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_reset.html', {"form": form})

