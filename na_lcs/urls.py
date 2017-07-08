from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^na_lcs$', views.na_lcs, name='na_lcs'),
    url(r'^about$', views.about, name='about'),
]