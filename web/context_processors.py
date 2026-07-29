from .models import ProfilSekolah


def profil_sekolah(request):
    profil = ProfilSekolah.objects.first()
    return {
        'profil': profil,
    }
