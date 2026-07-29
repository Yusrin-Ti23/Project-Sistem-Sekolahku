from . import views
from django.urls import path



urlpatterns = [

path("persetujuan/",views.daftar_persetujuan,name="persetujuan"),
path("aktifkan/<int:id>/",views.aktifkan_akun,name="aktifkan_akun"),
path("tolak/<int:id>/",views.tolak_akun,name="tolak_akun"),
path("register/guru/",views.register_guru,name="register_guru"),
path("register/siswa/",views.register_siswa,name="register_siswa"),

]

