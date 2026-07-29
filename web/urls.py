from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

path("verifikasi/",views.verifikasi_pengguna,name="verifikasi_pengguna"),
path("guru/aktif/<int:id>/",views.aktifkan_guru,name="aktifkan_guru"),
path("guru/tolak/<int:id>/",views.tolak_guru,name="tolak_guru"),
path("siswa/aktif/<int:id>/",views.aktifkan_siswa,name="aktifkan_siswa"),
path("siswa/tolak/<int:id>/",views.tolak_siswa,name="tolak_siswa"),
path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),




path("jadwal/edit/<int:id>/",views.edit_jadwal,name="edit_jadwal"),
path("jadwal/hapus/<int:id>/",views.hapus_jadwal,name="hapus_jadwal"),
path("jadwal/",views.jadwal_list,name="jadwal_list"),
path("jadwal/tambah/",views.tambah_jadwal,name="tambah_jadwal"),
path("jadwal/guru/",views.jadwal_guru,name="jadwal_guru"),
path("jadwal/siswa/",views.jadwal_siswa,name="jadwal_siswa"),

path("tahun/",views.tahun_list,name="tahun_list"),
path("tahun/tambah/",views.tahun_create,name="tahun_create"),

path("kelas/naik/",views.kelas_naik,name="kelas_naik",),
path("kelas/",views.kelas_list,name="kelas_list"),
path("kelas/tambah/",views.kelas_tambah,name="kelas_tambah"),
path("kelas/<int:id>/edit/",views.kelas_edit,name="kelas_edit"),
path("kelas/<int:id>/hapus/",views.kelas_hapus,name="kelas_hapus"),
path("kelas/<str:id>/",views.kelas_detail,name="kelas_detail"),

path("kelas/siswa/<str:kelas>/", views.daftar_siswa_per_kelas, name="daftar_siswa_per_kelas"),

path('', views.home, name='home'),

path('profil-sekolah/',views.profil_sekolah,name='profil_sekolah'),

# foto profil
path('profil/foto/', views.ubah_foto_profil, name='ubah_foto_profil'),

]
