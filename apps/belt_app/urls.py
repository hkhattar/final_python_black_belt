from django.conf.urls import url
from .import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$',views.register),
    url(r'^success$',views.success),
    url(r'^login$',views.login),
    url(r'^add_friend/(?P<id>\d+)$',views.add_friend),
    url(r'^show/(?P<id>\d+)$',views.show_friend),
    url(r'^remove/(?P<id>\d+)$',views.remove_friend),
    

]