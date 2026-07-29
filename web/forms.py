from django import forms
from .models import Guru, Siswa, Kelas, Jadwal, TahunAjaran
from .models import Jadwal

class TahunAjaranForm(forms.ModelForm):

    class Meta:

        model = TahunAjaran

        fields = "__all__"

        widgets = {

            "tahun": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),

            "semester": forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),

            "aktif": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input"
                }
            ),
        }


class JadwalForm(forms.ModelForm):

    class Meta:

        model = Jadwal

        fields = "__all__"

        widgets = {

            "hari": forms.Select(
                attrs={"class":"form-control"}
            ),

            "jam_mulai": forms.TimeInput(
                attrs={
                    "type":"time",
                    "class":"form-control"
                }
            ),

            "jam_selesai": forms.TimeInput(
                attrs={
                    "type":"time",
                    "class":"form-control"
                }
            ),

            "kelas": forms.Select(
                attrs={"class":"form-control"}
            ),

            "guru": forms.Select(
                attrs={"class":"form-control"}
            ),

            "mata_pelajaran": forms.TextInput(
                attrs={"class":"form-control"}
            ),

            "ruang": forms.TextInput(
                attrs={"class":"form-control"}
            ),

        }

class GuruForm(forms.ModelForm):
    class Meta:
        model = Guru
        fields = '__all__'


class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = '__all__'


class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = '__all__'
