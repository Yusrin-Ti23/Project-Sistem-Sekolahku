from django import forms
from .models import Nilai
from .models import Nilai, Absensi
from django import forms
from .models import Materi
from django import forms
from .models import Tugas, PengumpulanTugas
from django import forms
from .models import Tugas
from .models import Ujian
from .models import Soal


class SoalForm(forms.ModelForm):

    class Meta:

        model = Soal

        fields = [
            'nomor',
            'pertanyaan',
            'pilihan_a',
            'pilihan_b',
            'pilihan_c',
            'pilihan_d',
            'jawaban_benar',
            'pembahasan',
            'poin'
        ]

        widgets={

            'pertanyaan':forms.Textarea(
                attrs={'rows':4}
            ),

            'pembahasan':forms.Textarea(
                attrs={'rows':3}
            )

        }


class UjianForm(forms.ModelForm):

    class Meta:

        model = Ujian

        exclude = ["tahun_ajaran", "guru"]

        widgets = {

            'judul': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'mata_pelajaran': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'kelas': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'jurusan': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'semester': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'jenis': forms.Select(attrs={
                'class': 'form-control'
            }),

            'durasi': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'aktif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'tanggal_mulai': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),

            'tanggal_selesai': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),

        }

class TugasForm(forms.ModelForm):

    class Meta:

        model = Tugas

        fields = [
            'tahun_ajaran',
            'judul',
            'mata_pelajaran',
            'kelas',
            'deskripsi',
            'file_tugas',
            'deadline',
        ]

        widgets = {

            'kelas': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'deadline': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),

            'deskripsi': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['deadline'].input_formats = (
            '%Y-%m-%dT%H:%M',
        )


class PengumpulanTugasForm(forms.ModelForm):

    class Meta:
        model = PengumpulanTugas
        fields = ['file_jawaban']


class MateriForm(forms.ModelForm):

    class Meta:

        model = Materi

        fields = [
            'judul',
            'mata_pelajaran',
            'kelas',
            'deskripsi',
            'file'
        ]

class AbsensiForm(forms.ModelForm):

    class Meta:
        model = Absensi
        fields = [
            'siswa',
            'mata_pelajaran',
            'tanggal',
            'status',
            'keterangan'
        ]


class NilaiForm(forms.ModelForm):

    class Meta:

        model = Nilai

        fields = [
            'siswa',
            'mata_pelajaran',
            'tugas',
            'uts',
            'uas'
        ]