from django.urls import path

from . import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

router.register("guru", GuruViewSet)

router.register("siswa", SiswaViewSet)

router.register("kelas", KelasViewSet)

router.register("jadwal", JadwalViewSet)

router.register("tahunajaran", TahunAjaranViewSet)

router.register("materi", MateriViewSet)

router.register("tugas", TugasViewSet)

router.register("pengumpulantugas", PengumpulanTugasViewSet)

router.register("nilai", NilaiViewSet)

router.register("absensi", AbsensiViewSet)

router.register("berita", BeritaViewSet)

router.register("galeri", GaleriViewSet)

router.register("profilsekolah", ProfilSekolahViewSet)

router.register("profil", ProfilViewSet)

# Jika model Ujian sudah tersedia:
# router.register("ujian", UjianViewSet)


urlpatterns = [

    path("", include(router.urls)),

]

