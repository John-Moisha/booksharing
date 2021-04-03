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
from django.conf import settings
from django.conf.urls.static import static
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
    # url(r'^accounts/signup2/$', signup2, name='signup2'),

    path('accounts/activate/<uuid:username>/', ActivateView.as_view(), name='activate'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.a, name='activate'),
    # url(r'^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #             ActivateAccountView.as_view(), name='activate_account'),
    path('logs/', views.LogsMW.as_view(), name='logs'),
    path('__debug__/', include(debug_toolbar.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
