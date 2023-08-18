"""
URL configuration for Task project.

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
import profile
from django.urls import path
from Task.phone_auth.views import inviter_list, post_profile, get_profile, register, new_code, check_code


urlpatterns = [
    path('api/phone_auth/', register),
    path('api/phone_auth/', new_code),
    path('api/phone_auth/', check_code),
    path('api/profile/', get_profile),
    path('api/profile/', post_profile),
    path('api/inviter-list/', inviter_list),
]
