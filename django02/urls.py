"""django02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import account, pretty, admin


urlpatterns = [
    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    path('admin/list/',  admin.admin_list),
    path('admin/add/',  admin.admin_add),
    path('admin/<int:nid>/edit/',  admin.admin_edit),
    path('admin/<int:nid>/delete/',  admin.admin_delete),
    path('admin/<int:nid>/reset/',  admin.admin_reset),

    path('login/', account.account_login),
    path('logout/', account.account_logout),
    path('image/code/', account.image_code)
]
