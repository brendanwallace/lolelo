from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.nalcs, name='nalcs'),
    url(r'^about$', views.about, name='about'),
]