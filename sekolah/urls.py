"""
URL configuration for sekolah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from web import views
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path("api/",include("web.api.urls")),
    path("akun/",include("akun.urls")),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('guru/', views.guru, name='guru'),
    path('guru/tambah/', views.tambah_guru, name='tambah_guru'),
    path('guru/edit/<int:id>/', views.edit_guru, name='edit_guru'),
    path('guru/hapus/<int:id>/', views.hapus_guru, name='hapus_guru'),

    path('siswa/', views.siswa, name='siswa'),
    path('siswa/tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('siswa/edit/<int:id>/', views.edit_siswa, name='edit_siswa'),
    path('siswa/hapus/<int:id>/', views.hapus_siswa, name='hapus_siswa'),

    path('guru/pdf/',views.export_guru_pdf,name='guru_pdf'),
    path('siswa/pdf/',views.export_siswa_pdf,name='siswa_pdf'),

    path('berita/',views.berita,name='berita'),

    path('profil/',views.profil,name='profil'),
    path('galeri/',views.galeri,name='galeri'),
    path('kontak/',views.kontak,name='kontak'),

    path('dashboard/admin/',views.dashboard_admin,name='dashboard_admin'),

    path('dashboard/guru/',views.dashboard_guru,name='dashboard_guru'),

    path('dashboard/siswa/',views.dashboard_siswa,name='dashboard_siswa'),

    path('nilai/',include('akademik.urls')),
    path('', include('web.urls')),
    

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )