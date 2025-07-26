from django.urls import path
from . import views

app_name = "tree_menu"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('page/<path:page_name>/', views.page_view, name='page'),
    path('named-page/', views.named_page_view, name='named_page'),
    path('services-named/', views.services_view, name='services_named'),
    path('services-named/consulting/', views.consulting_view, name='consulting_named'),
    path('services-named/development/', views.development_view, name='development_named'),
]