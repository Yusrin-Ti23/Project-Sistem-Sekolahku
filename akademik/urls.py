from django.urls import path
from . import views

urlpatterns = [
    
    path('hasil-ujian/',views.hasil_semua,name='hasil_semua'),
    path('hasil-ujian/<int:id>/',views.hasil_ujian,name='hasil_ujian'),
    path('ujian/<int:id>/',views.mulai_ujian,name='mulai_ujian'),
    path('ujian-saya/',views.ujian_saya,name='ujian_saya'),
    path('ujian/<int:ujian_id>/soal/',views.daftar_soal,name='daftar_soal'),
    path('ujian/<int:ujian_id>/soal/tambah/',views.tambah_soal,name='tambah_soal'),
    path('soal/edit/<int:id>/',views.edit_soal,name='edit_soal'),
    path('soal/hapus/<int:id>/',views.hapus_soal,name='hapus_soal'),
    path('ujian/',views.daftar_ujian,name='daftar_ujian'),
    path('ujian/tambah/',views.tambah_ujian,name='tambah_ujian'),
    path('hasil-tugas/', views.nilai_tugas_saya, name='hasil_tugas'),
    path('tugas/<int:id>/pengumpulan/', views.daftar_pengumpulan, name='daftar_pengumpulan'),
    path('pengumpulan/<int:id>/nilai/', views.nilai_tugas, name='nilai_tugas'),
    path('pengumpulan/<int:id>/catatan/', views.catatan_guru, name='catatan_guru'),
    path('upload-jawaban/<int:id>/', views.upload_jawaban, name='upload_jawaban'),
    path('tugas-saya/', views.tugas_saya, name='tugas_saya'),
    path('tugas/', views.list_tugas, name='list_tugas'),
    path('tugas/tambah/', views.tambah_tugas, name='tambah_tugas'),
    path('tugas/edit/<int:id>/', views.edit_tugas, name='edit_tugas'),
    path('tugas/hapus/<int:id>/', views.hapus_tugas, name='hapus_tugas'),

    path('materi-saya/', views.materi_saya, name='materi_saya'),
    path('materi/<int:id>/lihat/', views.materi_detail, name='materi_detail'),
    path('materi/edit/<int:id>/', views.edit_materi, name='edit_materi'),
    path('materi/hapus/<int:id>/', views.hapus_materi, name='hapus_materi'),
    path('materi/', views.materi, name='materi'),
    path('materi/tambah/', views.tambah_materi, name='tambah_materi'),


    path('', views.daftar_nilai, name='daftar_nilai'),
    path('tambah/', views.tambah_nilai, name='tambah_nilai'),
    path('saya/', views.nilai_saya, name='nilai_saya'),

    path('rapor/', views.rapor_pdf, name='rapor_pdf'),
    path('ranking/', views.ranking, name='ranking'),

    path('absensi/', views.daftar_absensi, name='daftar_absensi'),
    path('absensi/tambah/', views.tambah_absensi, name='tambah_absensi'),
    path('absensi/saya/', views.absensi_saya, name='absensi_saya'),

    path('absensi/edit/<int:id>/', views.edit_absensi, name='edit_absensi'),
    path('absensi/hapus/<int:id>/', views.hapus_absensi, name='hapus_absensi'),
]


