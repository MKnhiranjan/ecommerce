"""
URL configuration for totodo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# main urls.py

from django.contrib import admin
from django.urls import path, include
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main,name="main"),
    path('user-monitoring/', views.user_monitoring, name='user_monitoring'), 
     path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
       path('add-user/', views.add_user, name='add_user'),
       path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
          path('user-login/', views.user_login, name='user_login'),
            path('admin-login/', views.admin_login, name='admin_login'),
               path('register/', views.user_register, name='user_register'),
        path('user-dashboard/', views.user_dashboard, name='dashboard'),
         path('add-product/', views.add_product_view, name='add_product'),
]
