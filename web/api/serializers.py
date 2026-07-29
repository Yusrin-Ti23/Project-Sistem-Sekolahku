from rest_framework import serializers
from web.models import Siswa
from rest_framework import serializers

from web.models import (
    Guru,
    Siswa,
    Kelas,
    Jadwal,
    TahunAjaran,
    Berita,
    Galeri,
    ProfilSekolah,
)

from akademik.models import (
    Materi,
    Tugas,
    PengumpulanTugas,
    Nilai,
    Absensi,
)

from akun.models import Profil
from akademik.models import Ujian



class GuruSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Guru
        fields = "__all__"


class KelasSerializer(serializers.ModelSerializer):

    wali_kelas = serializers.StringRelatedField()

    jumlah_siswa = serializers.SerializerMethodField()

    class Meta:
        model = Kelas
        fields = "__all__"

    def get_jumlah_siswa(self, obj):
        return obj.siswa.count()


class SiswaSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    kelas_nama = serializers.SerializerMethodField()

    class Meta:
        model = Siswa
        fields = "__all__"

    def get_kelas_nama(self, obj):
        if obj.kelas:
            return str(obj.kelas)
        return "-"


class JadwalSerializer(serializers.ModelSerializer):

    guru = serializers.StringRelatedField()

    kelas = serializers.StringRelatedField()

    tahun_ajaran = serializers.StringRelatedField()

    class Meta:
        model = Jadwal
        fields = "__all__"


class TahunAjaranSerializer(serializers.ModelSerializer):

    class Meta:
        model = TahunAjaran
        fields = "__all__"


class MateriSerializer(serializers.ModelSerializer):

    guru = serializers.StringRelatedField()

    kelas = serializers.StringRelatedField()

    class Meta:
        model = Materi
        fields = "__all__"


class TugasSerializer(serializers.ModelSerializer):

    guru = serializers.StringRelatedField()

    kelas = serializers.StringRelatedField()

    class Meta:
        model = Tugas
        fields = "__all__"


class PengumpulanTugasSerializer(serializers.ModelSerializer):

    siswa = serializers.StringRelatedField()

    tugas = serializers.StringRelatedField()

    class Meta:
        model = PengumpulanTugas
        fields = "__all__"


class NilaiSerializer(serializers.ModelSerializer):

    siswa = serializers.StringRelatedField()

    guru = serializers.StringRelatedField()

    class Meta:
        model = Nilai
        fields = "__all__"


class AbsensiSerializer(serializers.ModelSerializer):

    siswa = serializers.StringRelatedField()

    class Meta:
        model = Absensi
        fields = "__all__"


class UjianSerializer(serializers.ModelSerializer):

    guru = serializers.StringRelatedField()

    kelas = serializers.StringRelatedField()

    class Meta:
        model = Ujian
        fields = "__all__"


class BeritaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Berita
        fields = "__all__"


class GaleriSerializer(serializers.ModelSerializer):

    class Meta:
        model = Galeri
        fields = "__all__"


class ProfilSekolahSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilSekolah
        fields = "__all__"


class ProfilSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Profil
        fields = "__all__"