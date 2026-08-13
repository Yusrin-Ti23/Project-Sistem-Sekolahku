from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from web.models import Siswa, Guru, Kelas
from web.models import (
    Siswa,
    Guru,
    TahunAjaran,
    Kelas,
)


class Ujian(models.Model):


    JENIS = (
        ('UTS', 'UTS'),
        ('UAS', 'UAS'),
    )

    judul = models.CharField(max_length=200)

    mata_pelajaran = models.CharField(max_length=100)

    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    jurusan = models.CharField(max_length=50)

    semester = models.CharField(max_length=20)

    jenis = models.CharField(max_length=10,choices=JENIS)

    tahun_ajaran = models.ForeignKey(TahunAjaran,on_delete=models.PROTECT,null=True,blank=True)

    durasi = models.IntegerField(help_text="Menit")

    tanggal_mulai = models.DateTimeField()

    tanggal_selesai = models.DateTimeField()

    aktif = models.BooleanField(
        default=True
    )

    guru = models.ForeignKey(
        Guru,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.jenis} - {self.judul}"
    
class Soal(models.Model):

    ujian = models.ForeignKey(
        Ujian,
        on_delete=models.CASCADE,
        related_name='soal'
    )

    nomor = models.PositiveIntegerField()

    pertanyaan = models.TextField()

    pilihan_a = models.CharField(max_length=300)

    pilihan_b = models.CharField(max_length=300)

    pilihan_c = models.CharField(max_length=300)

    pilihan_d = models.CharField(max_length=300)

    jawaban_benar = models.CharField(
        max_length=1,
        choices=(
            ('A','A'),
            ('B','B'),
            ('C','C'),
            ('D','D'),
        )
    )

    pembahasan = models.TextField(
        blank=True,
        null=True
    )

    poin = models.IntegerField(
        default=1
    )

    class Meta:
        ordering = ['nomor']

    def __str__(self):
        return f"Soal {self.nomor}"
    
class HasilUjian(models.Model):

    ujian = models.ForeignKey(
        Ujian,
        on_delete=models.CASCADE
    )

    siswa = models.ForeignKey(
        'web.Siswa',
        on_delete=models.CASCADE
    )

    nilai = models.FloatField(
        default=0
    )

    benar = models.IntegerField(
        default=0
    )

    salah = models.IntegerField(
        default=0
    )

    tanggal = models.DateTimeField(
        auto_now_add=True
    )

    selesai = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.siswa.nama} - {self.ujian.judul}"




class JawabanSiswa(models.Model):



    PILIHAN = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    hasil = models.ForeignKey(
        HasilUjian,
        on_delete=models.CASCADE
    )

    soal = models.ForeignKey(
        Soal,
        on_delete=models.CASCADE
    )

    jawaban = models.CharField(
        max_length=1,
        choices=PILIHAN
    )

    benar = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.hasil.siswa.nama} - Soal {self.soal.nomor}"

    
class Tugas(models.Model):

    tahun_ajaran = models.ForeignKey(TahunAjaran,on_delete=models.PROTECT,
    null=True,
    blank=True
)
    judul = models.CharField(max_length=200)

    mata_pelajaran = models.CharField(max_length=100)

    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    deskripsi = models.TextField()

    file_tugas = models.FileField(
        upload_to='tugas/',
        blank=True,
        null=True
    )

    deadline = models.DateTimeField()

    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    guru = models.ForeignKey(
        Guru,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.judul


class PengumpulanTugas(models.Model):

    tugas = models.ForeignKey(
        Tugas,
        on_delete=models.CASCADE
    )

    siswa = models.ForeignKey(
        'web.Siswa',
        on_delete=models.CASCADE
    )

    guru = models.ForeignKey(
        Guru,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    file_jawaban = models.FileField(
        upload_to='jawaban/'
    )

    tanggal_upload = models.DateTimeField(
        auto_now_add=True
    )

    tanggal_dinilai = models.DateTimeField(
        null=True,
        blank=True
    )

    nilai = models.IntegerField(
        null=True,
        blank=True
    )

    catatan = models.TextField(
        blank=True,
        null=True
    )

    STATUS = (
        ('Belum Dinilai', 'Belum Dinilai'),
        ('Sudah Dinilai', 'Sudah Dinilai'),
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default='Belum Dinilai'
    )

    def __str__(self):
        return f"{self.siswa.nama} - {self.tugas.judul}"

class Materi(models.Model):

    tahun_ajaran = models.ForeignKey(
    TahunAjaran,
    on_delete=models.PROTECT,
    null=True,
    blank=True
)

    judul = models.CharField(
        max_length=200
    )

    mata_pelajaran = models.CharField(
        max_length=100
    )

    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    deskripsi = models.TextField()

    file = models.FileField(
        upload_to='materi/'
    )

    tanggal_upload = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.judul

class Absensi(models.Model):

    tahun_ajaran = models.ForeignKey(
    TahunAjaran,
    on_delete=models.PROTECT,
    null=True,
    blank=True
)

    STATUS_CHOICES = (
        ('Hadir', 'Hadir'),
        ('Izin', 'Izin'),
        ('Sakit', 'Sakit'),
        ('Alfa', 'Alfa'),
    )

    siswa = models.ForeignKey(
        'web.Siswa',
        on_delete=models.CASCADE
    )

    mata_pelajaran = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    tanggal = models.DateField(
        default=timezone.now
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    keterangan = models.TextField(
        blank=True,
        null=True
    )

    guru = models.ForeignKey(
        Guru,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.siswa.nama} - {self.mata_pelajaran} - {self.status}"
    
    

class Nilai(models.Model):

    tahun_ajaran = models.ForeignKey(
    TahunAjaran,
    on_delete=models.PROTECT,
    null=True,
    blank=True
)

    siswa = models.ForeignKey(
        Siswa,
        on_delete=models.CASCADE
    )

    guru = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE
    )

    mata_pelajaran = models.CharField(
        max_length=100
    )

    tugas = models.IntegerField()

    uts = models.IntegerField()

    uas = models.IntegerField()

    nilai_akhir = models.FloatField(
        blank=True,
        null=True
    )

    tanggal = models.DateField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        self.nilai_akhir = (
            self.tugas +
            self.uts +
            self.uas
        ) / 3

        super().save(
            *args,
            **kwargs
        )

    
    def __str__(self):
        return f"{self.siswa.nama} - {self.mata_pelajaran}"
    