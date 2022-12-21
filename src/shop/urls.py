from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/<str:slug>', views.filter_view, name='list'),
    path('filter/<str:slug>', views.filter_2_view, name='filter'),
    path('filter-2/<str:slug>/<str:pk>', views.filter_3_view, name='filter-2'),
    path('detail/<str:pk>', views.detail_view, name='detail'),
    # re_path(r'^list/(?P<slug>\w+)/$', views.filter_view, name='list'),
    path('signin/', views.login_view, name='signin'),
    path('signup/', views.register_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
