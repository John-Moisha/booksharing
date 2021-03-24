"""booksharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from books import views
from accounts.views import MyProfileView, ContactUsView, SignUpView, ActivateView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.Index.as_view(), name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('books/', include('books.urls')),
    # accounts
    path('accounts/my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('accounts/contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/activate/<uuid:username>/', ActivateView.as_view(), name='activate'),

    path('logs/', views.LogsMW.as_view(), name='logs'),
    path('__debug__/', include(debug_toolbar.urls)),

]
