from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/create$', views.add),
    url(r'^wish_items/(?P<id>\d+)$', views.show),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^create$', views.create),
    url(r'^favorite_item/(?P<id>\d+)$', views.favorite),
    url(r'^unfavorite_item/(?P<id>\d+)$', views.unfavorite),
    url(r'^logout$', views.logout),
]
