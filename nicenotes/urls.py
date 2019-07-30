"""nicenotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.routers import APIRootView
from rest_framework.authtoken.views import obtain_auth_token

from accounts.views import UserViewSet
from notes.views import NoteViewSet

note_list = NoteViewSet.as_view({
        'get': 'list',
        'post': 'create',
})

note_detail = NoteViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
})

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
        path('api/token/', obtain_auth_token, name='api-token'),
        path('api/users/', user_list, name='user-list'),
        path('api/users/me/', user_detail, name='user-detail'),
        path('api/notes/', note_list, name='note-list'),
        path('api/notes/<int:pk>/', note_detail, name='note-detail'),
        path('', TemplateView.as_view(template_name='notes/index.html'))
]
