from django.contrib import admin
from .models import Nilai, Absensi
from .models import Materi
from .models import Tugas, PengumpulanTugas
from .models import Ujian
from .models import Soal

admin.site.register(Ujian)
admin.site.register(Soal)

admin.site.register(Tugas)
admin.site.register(PengumpulanTugas)

admin.site.register(Materi)
admin.site.register(Nilai)
admin.site.register(Absensi)

