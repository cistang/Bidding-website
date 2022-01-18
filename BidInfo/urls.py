#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   urls.py    
@Contact :   tc.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/23 2:44 下午   tc      1.0         None
'''

# import lib
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search-form',views.search_form),
    path('search/',views.search),
    path('deepsearch-form/',views.deepsearch_form),
    path('deepsearch/',views.deepsearch)
]
