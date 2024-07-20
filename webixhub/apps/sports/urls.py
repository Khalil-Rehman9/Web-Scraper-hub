# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls.static import static
from django.urls import path, re_path
from apps.sports import views
from core import settings

urlpatterns = [

    # The sports home page
    path('boldtv', views.boldtv_index, name='boldtv_index'),
    path('edit/<int:id>',views.edit,name="boldtv_edit"),
    path('update/<int:id>',views.update,name="boldtv_update"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)