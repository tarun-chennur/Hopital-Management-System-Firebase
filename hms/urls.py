"""hms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from.import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.boot),
    url(r'^postsign/', views.postsign, name="postsign"),
    url(r'^senddocdata/', views.getdocdata),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^sendpatdata/', views.getpatdata),
    url(r'^patshow/', views.patshow, name="patshow"),
    url(r'^patview/', views.patview),
    url(r'^finaldoc/', views.finaldoc),
    url(r'^showyourdet/', views.showyourdet, name="showyourdet"),

   


]
