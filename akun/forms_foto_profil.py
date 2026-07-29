from django import forms

from .models import Profil
from web.models import Siswa, Guru


class FotoProfilForm(forms.ModelForm):
    """Form generik untuk upload foto profil (siswa/guru).

    View akan meng-instantiate form untuk model target sesuai role.
    """

    class Meta:
        model = Siswa
        fields = ["foto"]

        widgets = {
            "foto": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }


class FotoProfilGuruForm(forms.ModelForm):

    class Meta:
        model = Guru
        fields = ["foto"]
        widgets = {
            "foto": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }

