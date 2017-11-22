from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^users$', views.users),
    url(r'logout$', views.logout),
    url(r'quotes$', views.add_quote),
    url(r'add_quote$', views.add_quote),
    url(r'^add_fav/(?P<quote_id>\d+)$', views.add_fav),
    url(r'^unlike/(?P<quote_id>\d+)$', views.unlike),
    url(r'users/(?P<user_id>\d+)$', views.users)   
] 