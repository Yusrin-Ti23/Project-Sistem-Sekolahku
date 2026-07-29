from rest_framework.response import Response
from rest_framework.decorators import api_view

from web.models import Siswa
from .serializers import SiswaSerializer
from rest_framework import viewsets

from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter

from .serializers import *

from web.models import *

from akademik.models import *

from akun.models import Profil


@api_view(["GET"])
def siswa_api(request):

    siswa = Siswa.objects.all()

    serializer = SiswaSerializer(
        siswa,
        many=True
    )

    return Response(serializer.data)

class GuruViewSet(viewsets.ModelViewSet):

    queryset = Guru.objects.all()

    serializer_class = GuruSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [

        "nama",

        "nip",

    ]

    ordering_fields = [

        "nama",

        "nip"

    ]


class SiswaViewSet(viewsets.ModelViewSet):

    queryset = Siswa.objects.all()

    serializer_class = SiswaSerializer

    filter_backends = [

        DjangoFilterBackend,

        SearchFilter,

        OrderingFilter,

    ]

    filterset_fields = [

        "kelas",

        "jurusan",

        "status",

    ]

    search_fields = [

        "nama",

        "nis",

    ]

    ordering_fields = [

        "nama",

        "nis",

    ]


class KelasViewSet(viewsets.ModelViewSet):

    queryset = Kelas.objects.all()

    serializer_class = KelasSerializer

    filter_backends = [

        SearchFilter,

        OrderingFilter,

    ]

    search_fields = [

        "tingkat",

        "nama",

        "jurusan",

    ]


class JadwalViewSet(viewsets.ModelViewSet):

    queryset = Jadwal.objects.all()

    serializer_class = JadwalSerializer

    filter_backends = [

        SearchFilter,

        OrderingFilter,

    ]


class TahunAjaranViewSet(viewsets.ModelViewSet):

    queryset = TahunAjaran.objects.all()

    serializer_class = TahunAjaranSerializer


class MateriViewSet(viewsets.ModelViewSet):

    queryset = Materi.objects.all()

    serializer_class = MateriSerializer

    filter_backends = [

        SearchFilter,

        OrderingFilter,

    ]

    search_fields = [

        "judul",

    ]


class TugasViewSet(viewsets.ModelViewSet):

    queryset = Tugas.objects.all()

    serializer_class = TugasSerializer

    search_fields = [

        "judul",

    ]


class PengumpulanTugasViewSet(viewsets.ModelViewSet):

    queryset = PengumpulanTugas.objects.all()

    serializer_class = PengumpulanTugasSerializer


class NilaiViewSet(viewsets.ModelViewSet):

    queryset = Nilai.objects.all()

    serializer_class = NilaiSerializer


class AbsensiViewSet(viewsets.ModelViewSet):

    queryset = Absensi.objects.all()

    serializer_class = AbsensiSerializer


class UjianViewSet(viewsets.ModelViewSet):

    queryset = Ujian.objects.all()

    serializer_class = UjianSerializer


class BeritaViewSet(viewsets.ModelViewSet):

    queryset = Berita.objects.all()

    serializer_class = BeritaSerializer


class GaleriViewSet(viewsets.ModelViewSet):

    queryset = Galeri.objects.all()

    serializer_class = GaleriSerializer


class ProfilSekolahViewSet(viewsets.ModelViewSet):

    queryset = ProfilSekolah.objects.all()

    serializer_class = ProfilSekolahSerializer


class ProfilViewSet(viewsets.ModelViewSet):

    queryset = Profil.objects.all()

    serializer_class = ProfilSerializer