from django.conf.urls import include,url
from . import views

app_name='price'

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^portfolio/$', views.portfolio, name='portfolio'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
	url(r'^buy/(?P<company_symbol>[A-Z]+)/(?P<price>\d+\.\d{1,2})/$', views.buy, name='buy'),
	url(r'^sell/(?P<cs>[A-Z]+)/(?P<price>\d+\.\d{1,2})/$', views.sell, name='sell'),
	url(r'^(?P<company_symbol>[A-Z]+)/',views.detail,name='detail'),
]
