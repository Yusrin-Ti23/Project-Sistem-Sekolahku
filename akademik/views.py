from django.http import HttpResponse
try:
    from reportlab.pdfgen import canvas
except ModuleNotFoundError:  # allow server to run without reportlab
    canvas = None

from django.db.models import Avg
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from akun.decorators import role_required
from django.core.paginator import Paginator
from django.utils import timezone

from akun.models import Profil
from web.models import Siswa, Guru

from .models import (
    Nilai,
    Absensi,
    Materi,
    Tugas,
    PengumpulanTugas,
    Ujian,
    Soal,
    HasilUjian,
    JawabanSiswa,
)
from .forms import (
    NilaiForm,
    AbsensiForm,
    MateriForm,
    TugasForm,
    PengumpulanTugasForm,
    UjianForm,
    SoalForm,
)

import time
from web.models import TahunAjaran




@login_required
def hasil_semua(request):
    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    ujian_ids = Ujian.objects.filter(
        guru=guru
    ).values_list('id', flat=True)

    hasil = HasilUjian.objects.filter(
        ujian__in=ujian_ids
    ).select_related(
        "siswa",
        "ujian"
    )

    return render(
        request,
        "ujian/hasil_semua.html",
        {
            "hasil": hasil
        }
    )


@login_required
def hasil_ujian(request, id):

    hasil = get_object_or_404(
        HasilUjian,
        id=id
    )

    jawaban = JawabanSiswa.objects.filter(
        hasil=hasil
    ).select_related('soal')

    return render(
        request,
        'ujian/hasil.html',
        {
            'hasil': hasil,
            'jawaban': jawaban
        }
    )

@login_required
@role_required('siswa')
def mulai_ujian(request, id):


    ujian = get_object_or_404(
        Ujian,
        id=id
    )

    sekarang = timezone.now()
    print("=" * 60)
    print("Waktu Sekarang :", sekarang)
    print("Tanggal Mulai  :", ujian.tanggal_mulai)
    print("Tanggal Selesai:", ujian.tanggal_selesai)
    print("=" * 60)

    # Normalisasi waktu (penting kalau field tanggal_mulai/tanggal_selesai bisa tersimpan naive)
    tanggal_mulai = ujian.tanggal_mulai
    tanggal_selesai = ujian.tanggal_selesai

    if timezone.is_naive(tanggal_mulai):
        tanggal_mulai = timezone.make_aware(
            tanggal_mulai,
            timezone.get_current_timezone(),
        )

    if timezone.is_naive(tanggal_selesai):
        tanggal_selesai = timezone.make_aware(
            tanggal_selesai,
            timezone.get_current_timezone(),
        )

    # Pastikan sekarang juga timezone-aware
    if timezone.is_naive(sekarang):
        sekarang = timezone.make_aware(
            sekarang,
            timezone.get_current_timezone(),
        )

        print("=" * 60)
        print("Sekarang Lokal :", timezone.localtime(sekarang))
        print("Mulai Lokal    :", timezone.localtime(tanggal_mulai))
        print("Selesai Lokal  :", timezone.localtime(tanggal_selesai))
        print("=" * 60)

    if sekarang < tanggal_mulai:

        return render(
            request,
            "ujian/pesan.html",
            {"pesan": "Ujian belum dimulai."},
        )

    if sekarang > tanggal_selesai:
        return render(
            request,
            "ujian/pesan.html",
            {"pesan": "Waktu ujian sudah berakhir."},
        )



    siswa = get_object_or_404(
        Siswa,
        user=request.user
    )

    cek = HasilUjian.objects.filter(
        ujian=ujian,
        siswa=siswa
    ).exists()

    if cek:

        hasil = HasilUjian.objects.get(
            ujian=ujian,
            siswa=siswa
        )

        return redirect(
            "hasil_ujian",
            hasil.id
        )

    soal = Soal.objects.filter(
        ujian=ujian
    ).order_by("nomor")

    print("Jumlah soal :", soal.count())

    for s in soal:
        print(s.nomor, s.pertanyaan)

    if request.method == "POST":

        hasil = HasilUjian.objects.create(
            ujian=ujian,
            siswa=siswa
        )

        benar = 0
        salah = 0

        for s in soal:

            jawaban = request.POST.get(
                f"soal{s.id}"
            )

            if jawaban:

                status = (
                    jawaban ==
                    s.jawaban_benar
                )

                JawabanSiswa.objects.create(
                    hasil=hasil,
                    soal=s,
                    jawaban=jawaban,
                    benar=status
                )

                if status:
                    benar += 1
                else:
                    salah += 1

        total = soal.count()

        if total > 0:
            nilai = (benar / total) * 100
        else:
            nilai = 0

        hasil.benar = benar
        hasil.salah = salah
        hasil.nilai = nilai
        hasil.selesai = True
        hasil.save()

        # Sinkronkan nilai ujian otomatis ke Nilai (akademik)
        # Mapping:
        # - UTS -> field `uts`
        # - UAS -> field `uas`
        # - Tugas -> tetap 0 (diisi dari penilaian tugas)
        guru_obj = Guru.objects.first()
        if guru_obj is None:
            # Jika belum ada data guru di database, skip agar tidak error 500
            return redirect("hasil_ujian", hasil.id)

        nilai_kwargs = {
            "tugas": 0,
            "uts": 0,
            "uas": 0,
        }
        if ujian.jenis == "UTS":
            nilai_kwargs["uts"] = nilai
        elif ujian.jenis == "UAS":
            nilai_kwargs["uas"] = nilai

        # Jangan overwrite nilai tugas saat submit ujian.
        # Jadi hanya update kolom `uts`/`uas` yang sesuai jenis ujian.
        defaults = nilai_kwargs
        # Ambil record Nilai yang sudah ada (kalau ada), supaya kolom `tugas`
        # yang diinput guru lewat penilaian tugas tidak tertimpa oleh nilai ujian.
        # KUNCI agar tidak membuat baris baru: samakan kombinasi unique yang dipakai
        # di data nilai akademik.
        nilai_exist = Nilai.objects.filter(
            siswa=siswa,
            mata_pelajaran=ujian.mata_pelajaran,
        ).first()

        if nilai_exist is not None:
            defaults["tugas"] = nilai_exist.tugas

        # Selalu update baris yang ada berdasarkan (siswa, mata_pelajaran).
        # Field `guru` diisi dari guru pertama yang tersedia (untuk memenuhi FK),
        # tapi tidak dipakai sebagai kunci update supaya tidak terbentuk baris dobel.
        nilai_obj, created = Nilai.objects.update_or_create(
            siswa=siswa,
            mata_pelajaran=ujian.mata_pelajaran,
            defaults={
                **defaults,
                "guru": guru_obj,
            },
        )

        return redirect(
            "hasil_ujian",
            hasil.id
        )

    # Kirim waktu selesai ke frontend dalam epoch (ms) supaya timer akurat.
    # tanggal_selesai sudah dinormalisasi menjadi timezone-aware di atas.
    waktu_selesai = tanggal_selesai
    waktu_selesai_epoch_ms = int(waktu_selesai.timestamp() * 1000)

    return render(
        request,
        "ujian/mulai.html",
        {
            "ujian": ujian,
            "soal": soal,
            "waktu_selesai": waktu_selesai,
            "waktu_selesai_epoch_ms": waktu_selesai_epoch_ms,
        },
    )


    # Kirim waktu selesai ke frontend dalam epoch (ms) supaya timer tidak salah akibat timezone\r\n    # dan format string.\r\n    waktu_selesai = ujian.tanggal_selesai\r\n    if timezone.is_naive(waktu_selesai):\r\n        waktu_selesai = timezone.make_aware(\r\n            waktu_selesai,\r\n            timezone.get_current_timezone(),\r\n        )\r\n\r\n    waktu_selesai_epoch_ms = int(waktu_selesai.timestamp() * 1000)\r\n\r\n    return render(\r\n        request,\r\n        "ujian/mulai.html",\r\n        {\r\n            "ujian": ujian,\r\n            "soal": soal,\r\n            "waktu_selesai": waktu_selesai,\r\n            "waktu_selesai_epoch_ms": waktu_selesai_epoch_ms,\r\n        },\r\n    )\r\n



@login_required
def ujian_saya(request):

    siswa = get_object_or_404(
        Siswa,
        user=request.user
    )

    daftar_ujian = Ujian.objects.filter(
        kelas=siswa.kelas,
        aktif=True
    ).order_by("tanggal_mulai")

    data = []

    for u in daftar_ujian:

        hasil = HasilUjian.objects.filter(
            ujian=u,
            siswa=siswa
        ).first()

        data.append({

            "ujian": u,

            "hasil": hasil

        })

    return render(

        request,

        "ujian/ujian_saya.html",

        {

            "data": data

        }

    )

@login_required
def hapus_soal(request,id):

    soal=get_object_or_404(
        Soal,
        id=id
    )

    ujian=soal.ujian

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if ujian.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    ujian_id = ujian.id
    soal.delete()

    return redirect(
        'daftar_soal',
        ujian_id
    )

@login_required
def edit_soal(request,id):

    soal=get_object_or_404(
        Soal,
        id=id
    )

    ujian = soal.ujian

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if ujian.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    form=SoalForm(
        request.POST or None,
        instance=soal
    )

    if form.is_valid():

        form.save()

        return redirect(
            'daftar_soal',
            ujian.id
        )

    return render(
        request,
        'soal/form.html',
        {
            'form':form,
            'ujian': ujian
        }
    )

@login_required
def tambah_soal(request, ujian_id):

    ujian = get_object_or_404(
        Ujian,
        id=ujian_id
    )

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if ujian.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    soal_terakhir = Soal.objects.filter(
        ujian=ujian
    ).order_by('-nomor').first()

    nomor_awal = (soal_terakhir.nomor + 1) if soal_terakhir else 1

    form = SoalForm(
        request.POST or None,
        initial={'nomor': nomor_awal}
    )

    if form.is_valid():

        data = form.save(commit=False)

        data.ujian = ujian

        data.save()

        return redirect(
            'daftar_soal',
            ujian.id
        )

    return render(
        request,
        'soal/form.html',
        {
            'form': form,
            'ujian': ujian
        }
    )


@login_required
def daftar_soal(request, ujian_id):

    ujian = get_object_or_404(
        Ujian,
        id=ujian_id
    )

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if ujian.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    soal = Soal.objects.filter(
        ujian=ujian
    )

    return render(
        request,
        'soal/list.html',
        {
            'ujian': ujian,
            'soal': soal,
            'total': soal.count()
        }
    )


@login_required
def tambah_ujian(request):
    form = UjianForm(request.POST or None)

    if form.is_valid():
        tahun = TahunAjaran.objects.filter(aktif=True).first()

        if tahun is None:
            return HttpResponse("Belum ada Tahun Ajaran yang aktif.")

        ujian = form.save(commit=False)
        ujian.tahun_ajaran = tahun

        guru = get_object_or_404(
            Guru,
            user=request.user
        )
        ujian.guru = guru

        ujian.save()

        return redirect("daftar_ujian")

    return render(
        request,
        'ujian/form.html',
        {
            'form': form
        }
    )


@login_required
def daftar_ujian(request):
    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    data = Ujian.objects.filter(
        guru=guru
    ).order_by('-tanggal_mulai')

    return render(
        request,
        'ujian/list.html',
        {
            'ujian':data
        }
    )


@login_required
def nilai_tugas_saya(request):

    siswa = Siswa.objects.get(
        user=request.user
    )

    data = PengumpulanTugas.objects.filter(
        siswa=siswa
    ).select_related('tugas', 'guru')


    return render(
    request,
    'tugas/hasil_tugas.html',
    {
        'data': data
    }
)


@login_required
def catatan_guru(request, id):
    pengumpulan = get_object_or_404(PengumpulanTugas, id=id)

    # Keamanan: hanya siswa pemilik yang boleh melihat catatannya
    siswa = get_object_or_404(Siswa, user=request.user)
    if pengumpulan.siswa_id != siswa.id:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    return render(
        request,
        'tugas/catatan_guru.html',
        {
            'pengumpulan': pengumpulan,
            'catatan': pengumpulan.catatan,
        },
    )



@login_required
def nilai_tugas(request, id):
    pengumpulan = get_object_or_404(PengumpulanTugas, id=id)

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if pengumpulan.tugas.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    if request.method == 'POST':
        nilai = request.POST.get('nilai')
        catatan = request.POST.get('catatan')
        guru_nama = (request.POST.get('guru') or '').strip()

        if guru_nama:
            guru_obj = Guru.objects.filter(nama=guru_nama).first()
            if not guru_obj:
                guru_obj = Guru.objects.create(
                    nama=guru_nama,
                    mata_pelajaran=pengumpulan.tugas.mata_pelajaran,
                    email='unknown@example.com',
                )
            pengumpulan.guru = guru_obj

        pengumpulan.nilai = int(nilai) if nilai is not None and nilai != '' else None
        pengumpulan.catatan = catatan
        pengumpulan.status = 'Sudah Dinilai'
        pengumpulan.tanggal_dinilai = timezone.now()
        pengumpulan.save()

        # Simpan juga ke model Nilai.
        # Karena Nilai model memiliki kolom tugas/uts/uas, sementara nilai dari form dipakai sebagai `tugas`.
        # Update berdasarkan (siswa, mata_pelajaran) agar tidak membuat baris Nilai baru
        # hanya karena guru berbeda.
        nilai_obj = Nilai.objects.filter(
            siswa=pengumpulan.siswa,
            mata_pelajaran=pengumpulan.tugas.mata_pelajaran,
        ).first()

        if nilai_obj is None:
            Nilai.objects.create(
                siswa=pengumpulan.siswa,
                guru=pengumpulan.guru,
                mata_pelajaran=pengumpulan.tugas.mata_pelajaran,
                tugas=pengumpulan.nilai or 0,
                uts=0,
                uas=0,
            )
        else:
            nilai_obj.guru = pengumpulan.guru
            nilai_obj.tugas = pengumpulan.nilai or 0
            # jangan ubah uts/uas di sini
            nilai_obj.save()

        return redirect('daftar_pengumpulan', id=pengumpulan.tugas.id)


    return render(
        request,
        'tugas/nilai.html',
        {
            'pengumpulan': pengumpulan,
        },
    )


# (Perbaikan) Kode berikut sebelumnya keliru berada di level modul.
# Proses penilaian harus berada di dalam fungsi view.



@login_required
def daftar_pengumpulan(request, id):

    tugas = get_object_or_404(
        Tugas,
        id=id
    )

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if tugas.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    data = PengumpulanTugas.objects.filter(
        tugas=tugas
    ).select_related('siswa')

    return render(
        request,
        'tugas/pengumpulan.html',
        {
            'tugas': tugas,
            'data': data
        }
    )

@login_required
def upload_jawaban(request, id):

    tugas = get_object_or_404(Tugas, id=id)

    siswa = get_object_or_404(
        Siswa,
        user=request.user
    )

    if request.method == 'POST':

        form = PengumpulanTugasForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            jawaban = form.save(commit=False)

            jawaban.tugas = tugas

            jawaban.siswa = siswa

            jawaban.save()

            return redirect('tugas_saya')

    else:

        form = PengumpulanTugasForm()

    return render(
        request,
        'tugas/upload_jawaban.html',
        {
            'form': form,
            'tugas': tugas
        }
    )

@login_required
def tugas_saya(request):

    try:
        siswa = Siswa.objects.get(user=request.user)

        tugas = Tugas.objects.filter(
            kelas=siswa.kelas
        ).order_by('deadline')

        # Tambahkan penanda untuk status di UI siswa.
        # Indikator: sudah ada record PengumpulanTugas untuk (tugas, siswa).
        pengumpulan_exist = (
            PengumpulanTugas.objects.filter(
                siswa=siswa,
                tugas__in=tugas,
            )
            .values_list('tugas_id', flat=True)
        )
        pengumpulan_exist = set(pengumpulan_exist)

        for t in tugas:
            if t.id in pengumpulan_exist:
                t.status_tugas = 'Tugas telah dikerjakan dan terkirim ke guru'
            else:
                t.status_tugas = 'Tugas belum dikerjakan'

    except Siswa.DoesNotExist:
        tugas = []

    return render(
        request,
        'tugas/tugas_saya.html',
        {
            'tugas': tugas
        }
    )



@login_required
def hapus_tugas(request, id):

    tugas = get_object_or_404(
        Tugas,
        id=id
    )

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if tugas.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    tugas.delete()

    return redirect(
        'list_tugas'
    )

@login_required
def edit_tugas(request, id):

    tugas = get_object_or_404(
        Tugas,
        id=id
    )

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if tugas.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    if request.method == 'POST':

        form = TugasForm(
            request.POST,
            request.FILES,
            instance=tugas
        )

        if form.is_valid():

            form.save()

            return redirect(
                'list_tugas'
            )

    else:

        form = TugasForm(
            instance=tugas
        )

    return render(
        request,
        'tugas/form.html',
        {
            'form': form,
            'judul': 'Edit Tugas'
        }
    )


@login_required
def tambah_tugas(request):

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if request.method == 'POST':

        form = TugasForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            tugas = form.save(commit=False)
            tugas.guru = guru
            tugas.save()

            return redirect(
                'list_tugas'
            )

    else:

        form = TugasForm()

    return render(
        request,
        'tugas/form.html',
        {
            'form': form,
            'judul': 'Tambah Tugas'
        }
    )


@login_required
def list_tugas(request):

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    tugas = Tugas.objects.filter(
        guru=guru
    ).order_by('-tanggal_dibuat')

    return render(
        request,
        'tugas/list.html',
        {
            'tugas': tugas
        }
    )


@login_required
def materi_saya(request):
    try:
        siswa = Siswa.objects.get(user=request.user)
        materi = Materi.objects.filter(kelas=siswa.kelas).order_by('-tanggal_upload')
        total_materi = materi.count()
    except Siswa.DoesNotExist:
        materi = []
        total_materi = 0

    return render(
        request,
        'materi/materi_saya.html',
        {
            'materi': materi,
            'total_materi': total_materi,
        },
    )


@login_required
def materi_detail(request, id):
    materi = get_object_or_404(Materi, id=id)

    # Validasi akses: siswa hanya boleh melihat materi kelasnya sendiri
    try:
        siswa = Siswa.objects.get(user=request.user)
    except Siswa.DoesNotExist:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    if materi.kelas != siswa.kelas:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    # Preview sederhana untuk file PDF (iframe). Format lain biasanya tidak bisa di-preview penuh.
    preview_url = None
    try:
        filename = materi.file.name.lower()
        if filename.endswith('.pdf'):
            preview_url = materi.file.url
    except Exception:
        preview_url = None

    return render(
        request,
        'materi/materi_detail.html',
        {
            'materi': materi,
            'preview_url': preview_url,
        },
    )


def hapus_materi(request, id):
    Materi.objects.filter(id=id).delete()
    return redirect('materi')



def edit_materi(request, id):
    materi = Materi.objects.get(id=id)
    form = MateriForm(instance=materi)

    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES, instance=materi)

        if form.is_valid():
            form.save()
            return redirect('materi')

    return render(request, 'materi/form.html', {'form': form})


def materi(request):
    keyword = request.GET.get('q')

    data = Materi.objects.all().order_by('-tanggal_upload')

    if keyword:
        data = data.filter(judul__icontains=keyword)

    total_materi = data.count()

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    materi_page = paginator.get_page(page_number)

    return render(
        request,
        'materi/list.html',
        {
            'materi': materi_page,
            'total_materi': total_materi,
        },
    )


def tambah_materi(request):
    form = MateriForm()

    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('materi')

    return render(request, 'materi/form.html', {'form': form})


@login_required
def absensi_saya(request):
    siswa = Siswa.objects.get(user=request.user)
    data = Absensi.objects.filter(siswa=siswa)

    return render(
        request,
        'absensi/saya.html',
        {
            'absensi': data,
        },
    )


@login_required
def tambah_absensi(request):
    initial = {}

    mata_pelajaran = request.GET.get('mata_pelajaran')
    if mata_pelajaran:
        initial['mata_pelajaran'] = mata_pelajaran

    if request.method == 'POST':
        form = AbsensiForm(request.POST)
        if form.is_valid():
            absensi = form.save(commit=False)
            guru = get_object_or_404(
                Guru,
                user=request.user
            )
            absensi.guru = guru
            absensi.save()
            return redirect('daftar_absensi')
    else:
        form = AbsensiForm(initial=initial)

    return render(
        request,
        'absensi/form.html',
        {
            'form': form,
        },
    )


@login_required
def daftar_absensi(request):
    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    data = Absensi.objects.filter(
        guru=guru
    ).select_related('siswa').order_by('-tanggal')

    return render(
        request,
        'absensi/list.html',
        {
            'absensi': data,
        },
    )


@login_required
def edit_absensi(request, id):
    absensi = get_object_or_404(Absensi, id=id)

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if absensi.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    if request.method == 'POST':
        form = AbsensiForm(request.POST, instance=absensi)
        if form.is_valid():
            form.save()
            return redirect('daftar_absensi')
    else:
        form = AbsensiForm(instance=absensi)

    return render(request, 'absensi/form.html', {'form': form})


@login_required
def hapus_absensi(request, id):
    absensi = get_object_or_404(Absensi, id=id)

    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    if absensi.guru != guru:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    absensi.delete()
    return redirect('daftar_absensi')




@login_required
def rapor_pdf(request):
    siswa = Siswa.objects.get(user=request.user)
    nilai = Nilai.objects.filter(siswa=siswa)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapor.pdf"'

    if canvas is None:
        return HttpResponse("reportlab tidak terpasang di environment ini.", status=500)

    p = canvas.Canvas(response)

    p.drawString(100, 800, f'Rapor {siswa.nama}')

    y = 750
    for n in nilai:
        p.drawString(50, y, f'{n.mata_pelajaran} : {n.nilai_akhir}')
        y -= 20

    p.save()
    return response


@login_required
def ranking(request):
    ranking_data = (
        Nilai.objects.values('siswa__nama')
        .annotate(rata_rata=Avg('nilai_akhir'))
        .order_by('-rata_rata')
    )

    return render(
        request,
        'nilai/rangking.html',
        {
            'ranking': ranking_data,
        },
    )



@login_required
def nilai_saya(request):
    profil = Profil.objects.get(user=request.user)

    if profil.role != 'siswa':
        return redirect('login')

    siswa = Siswa.objects.get(user=request.user)
    data_nilai = Nilai.objects.filter(siswa=siswa)

    return render(
        request,
        'nilai/nilai_saya.html',
        {
            'nilai': data_nilai,
        },
    )


@login_required
def daftar_nilai(request):
    guru = get_object_or_404(
        Guru,
        user=request.user
    )

    data = Nilai.objects.filter(
        guru=guru
    )

    return render(
        request,
        'nilai/list.html',
        {
            'nilai': data,
        },
    )


@login_required
def tambah_nilai(request):
    form = NilaiForm(request.POST or None)

    if form.is_valid():
        nilai = form.save(commit=False)
        guru = get_object_or_404(
            Guru,
            user=request.user
        )
        nilai.guru = guru
        nilai.save()
        return redirect('daftar_nilai')

    return render(request, 'nilai/form.html', {'form': form})

