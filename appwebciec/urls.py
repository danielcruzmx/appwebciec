"""appwebciec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    url(r'^api-rest/olimpo/informe/(?P<depto_id>[\w]+)/$',
    views.CuotasViewSet.as_view(), name='my_rest_view'),
	url(r'^api-rest/totalIngresosEgresos/(?P<condominio>[\w]+)/(?P<fec_ini>((19|20)\d\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))/(?P<fec_fin>((19|20)\d\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))/$',
    views.TotalIngresosEgresosViewSet.as_view(), name='my_rest_view'),
    url(r'^api-rest/cuotasDeptoMes/(?P<condominio>[\w]+)/(?P<mes_anio>(0?[1-9]|1[012])-((19|20)\d\d))/$',
    views.CuotasDeptoMesViewSet.as_view(), name='my_rest_view'),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^explorer/', include('explorer.urls')),
]

urlpatterns += staticfiles_urlpatterns()