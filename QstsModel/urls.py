"""
URL configuration for QstsModel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from qstsapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.acceuil, name=''),
    path('qstsapi/', views.qstsapi, name='qstsapi'),
    path('gradesapi/', views.gradesapi, name='gradesapi'),
    path('algo/',views.calcul_moyenne.as_view()),
    path('model/', views.call_model.as_view()),
    path('myAPI/', views.chatbot_api_view, name='chatbot_api')
]
