from django.contrib import admin
from .models import (
    Guru,
    Siswa,
    Kelas,
    Berita,
    Galeri,
    ProfilSekolah,
)

from .models import Jadwal
from .models import TahunAjaran



admin.site.register(TahunAjaran)
admin.site.register(Jadwal)
admin.site.register(Kelas)
admin.site.register(Guru)
admin.site.register(Siswa)
admin.site.register(Berita)
admin.site.register(Galeri)
admin.site.register(ProfilSekolah)