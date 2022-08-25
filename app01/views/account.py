from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse

from app01 import models
from app01.utils.code import check_code

from app01.utils.form import AccountModelForm


def account_login(request):
    """ 登录 """
    if request.method == "GET":
        form = AccountModelForm()
        return render(request, 'login.html', {"form": form})

    form = AccountModelForm(data=request.POST)
    if form.is_valid():

        # 验证码的校验,pop是顺便把 code表项剔除掉 方便后期使用**form.cleaned_data搜索
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        # 全转换为大写
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        if models.Admin.objects.filter(adminName=form.cleaned_data.get("adminName")).exists():
            obj = models.Admin.objects.filter(adminName=form.cleaned_data.get("adminName")).first()
            if obj.password == form.cleaned_data.get("password"):

                # 用户名和密码正确
                # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
                request.session["info"] = {'id': obj.id, 'name': obj.adminName}
                # session可以保存7天
                request.session.set_expiry(60 * 60 * 24 * 7)

                return redirect('/pretty/list/')

            form.add_error("password", "用户名或密码错误")
        form.add_error("password", "用户名或密码错误")

    return render(request, 'login.html', {"form": form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    # 写入内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def account_logout(request):
    """ 注销 """
    request.session.clear()

    return redirect('/login/')