from todoist import views
from django.conf import settings
from django.conf.urls import include,url

urls = [
    url(r'index/$', views.index),
    url(r'index/lists/$', views.list_serializer),
    url(r'lists/(?P<pk>[0-9]+)/$', views.list_serializer_detail),
    url(r'items/(?P<pk>[0-9]+)/$', views.item_serializer_detail),
    url(r'lists/(?P<pk>[0-9]+)/items/$', views.list_id_item_serializer_detail1),
    url(r'lists/items/$', views.list_id_item_serializer_detail),

]