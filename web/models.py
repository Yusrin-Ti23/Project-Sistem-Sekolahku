from django.db import models
from django.contrib.auth.models import User


# NOTE:
# `wali_kelas` butuh model `Guru`, jadi pastikan referensi `Guru` sudah ada di file.
# Penempatan ulang kelas berikut dilakukan untuk menghilangkan warning Pylance.


class Guru(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nama = models.CharField(max_length=100)

    nip = models.CharField(max_length=50, null=True, blank=True)


    mata_pelajaran = models.CharField(max_length=100)


    email = models.EmailField()

    foto = models.ImageField(
        upload_to='guru/',
        null=True,
        blank=True
    )
    STATUS = (
    ("Menunggu", "Menunggu"),
    ("Aktif", "Aktif"),
    ("Ditolak", "Ditolak"),
    )

    status = models.CharField(
    max_length=20,
    choices=STATUS,
    default="Menunggu"
    )

    def __str__(self):
        return self.nama


class Kelas(models.Model):
    TINGKAT = (
        ("X", "X"),
        ("XI", "XI"),
        ("XII", "XII"),
    )

    tingkat = models.CharField(
        max_length=5,
        choices=TINGKAT
    )

    nama = models.CharField(
        max_length=30
    )

    jurusan = models.CharField(
        max_length=50
    )

    wali_kelas = models.ForeignKey(
        "Guru",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
       return f"{self.tingkat} {self.nama} {self.jurusan}"  

class ProfilSekolah(models.Model):

    nama_sekolah = models.CharField(
        max_length=200
    )

    logo = models.ImageField(
        upload_to='profil/',
        null=True,
        blank=True
    )

    alamat = models.TextField()

    telepon = models.CharField(
        max_length=30
    )

    email = models.EmailField()

    website = models.URLField(
        blank=True,
        null=True
    )

    visi = models.TextField()

    misi = models.TextField()

    def __str__(self):
        return self.nama_sekolah
    

class Siswa(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nama = models.CharField(max_length=100)

    nis = models.CharField(max_length=50, null=True, blank=True)

    kelas = models.ForeignKey(
    Kelas,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="siswa"
    )

    jurusan = models.CharField(max_length=50)


    foto = models.ImageField(
        upload_to='siswa/',
        null=True,
        blank=True
    )

    STATUS = (
    ("Menunggu","Menunggu"),
    ("Aktif","Aktif"),
    ("Ditolak","Ditolak"),
    )

    status = models.CharField(
    max_length=20,
    choices=STATUS,
    default="Menunggu"
    )

    def __str__(self):
        return self.nama




class Galeri(models.Model):

    judul = models.CharField(
        max_length=200
    )

    gambar = models.ImageField(
        upload_to='galeri/'
    )

    tanggal = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.judul

class Berita(models.Model):

    judul = models.CharField(max_length=200)
    isi = models.TextField()
    gambar = models.ImageField(upload_to='berita/',null=True,blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul
    
    
class TahunAjaran(models.Model):

    SEMESTER = (
        ("Ganjil", "Ganjil"),
        ("Genap", "Genap"),
    )

    tahun = models.CharField(
        max_length=20
    )

    semester = models.CharField(
        max_length=10,
        choices=SEMESTER
    )

    aktif = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.tahun} - {self.semester}"
    
    
class Jadwal(models.Model):

        HARI = (
        ("Senin", "Senin"),
        ("Selasa", "Selasa"),
        ("Rabu", "Rabu"),
        ("Kamis", "Kamis"),
        ("Jumat", "Jumat"),
        ("Sabtu", "Sabtu"),
    )

        hari = models.CharField(
        max_length=20,
        choices=HARI
    )

        jam_mulai = models.TimeField()

        jam_selesai = models.TimeField()

        kelas = models.ForeignKey(
        Kelas,
        on_delete=models.CASCADE
    )

        guru = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE
    )

        mata_pelajaran = models.CharField(
        max_length=100
    )

        ruang = models.CharField(
        max_length=50
    )

        tahun_ajaran = models.ForeignKey(
    TahunAjaran,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    

        def __str__(self):
            return f"{self.hari} {self.mata_pelajaran}"


