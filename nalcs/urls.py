from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # legacy -- eventually remove this:
    url(r'^na_lcs$', views.na_lcs, name='na_cls'),
    url(r'^nalcs$', views.nalcs, name='nalcs'),
    url(r'^about$', views.about, name='about'),
]