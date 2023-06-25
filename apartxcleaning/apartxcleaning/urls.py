"""proptech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from apartxapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_order/', views.add_order, name='add_order'),
    path('send_request/<int:order_id>/', views.send_request, name='send_request'),
    path('accept_request/<int:order_id>/', views.accept_request, name='accept_request'),
    path('view_order/<int:order_id>/', views.view_order, name='view_order'),
    path('completed/<int:order_id>/', views.completed, name='completed'),
    path('worker_profile/<int:worker_id>/', views.workerprofile, name='worker_profile'),
    path('add_free_time', views.add_free_time, name='add_free_time'),
    path('map', views.map, name='map'),

    # authentication
    path('signup/', views.signupsystem, name='signupsystem'),
    path('login', views.loginsystem, name='loginsystem'),
    path('logout/', views.logoutsystem, name='logoutsystem'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
