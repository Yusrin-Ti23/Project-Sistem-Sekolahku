from django import forms
from django.contrib.auth.models import User
from .models import Profil
from web.models import Kelas


class RegisterGuruForm(forms.ModelForm):

    nip = forms.CharField(label="NIP")

    mata_pelajaran = forms.CharField(label="Mata Pelajaran")


    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
    )


    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Konfirmasi Password",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "username",
            "email",
            "password",
        ]

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("password2")

        if pw1 and pw2 and pw1 != pw2:
            self.add_error("password2", "Konfirmasi password tidak sama")

        return cleaned_data



class RegisterSiswaForm(forms.ModelForm):


    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    # Tambahan data siswa
    nis = forms.CharField(label="Nis")

    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(),
        label="Kelas"
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "nis",
            "username",
            "email",
            "password",
            "kelas",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ubah label `first_name` menjadi nama lengkap
        self.fields["first_name"].label = "Nama Lengkap"

