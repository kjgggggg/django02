from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import OrderModelForm
from app01.utils.pagination import Pagination


def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ 构造柱状图的数据 """
    # 数据可以去数据库中获取
    legend = ["梁吉宁", "武沛齐"]
    series_list = [
        {
            "name": '梁吉宁',
            "type": 'bar',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": '武沛齐',
            "type": 'bar',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)