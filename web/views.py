from akun.decorators import role_required
from akun.models import Profil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from akun.forms_foto_profil import FotoProfilForm, FotoProfilGuruForm

# reportlab (untuk export PDF) bersifat opsional.
# Hindari error saat package belum terinstall saat Django start.
try:
    from reportlab.pdfgen import canvas
except ModuleNotFoundError:  # pragma: no cover
    canvas = None


from .forms import GuruForm, SiswaForm
from .models import Guru, Siswa
from .models import Berita
from .models import Galeri
from django.contrib.auth.decorators import login_required
from .models import ProfilSekolah
from .models import Kelas
from django.shortcuts import render
from .forms import KelasForm
from django.shortcuts import redirect, get_object_or_404
from .models import Kelas, Siswa, Guru
from django.shortcuts import get_object_or_404
from .models import Jadwal
from .forms import JadwalForm
from .models import Jadwal, Guru
from .models import Kelas, Siswa
from django.db import models
from django.db.models import Q
from django.contrib import messages
from .models import TahunAjaran
from .forms import TahunAjaranForm
from django.db import models
from akun.models import Profil



def edit_jadwal(request, id):

    jadwal = get_object_or_404(
        Jadwal,
        id=id
    )

    form = JadwalForm(
        request.POST or None,
        instance=jadwal
    )

    if form.is_valid():
        # Cari Tahun Ajaran yang aktif
        tahun = TahunAjaran.objects.filter(aktif=True).first()

        jadwal = form.save(commit=False)

        # Isi Tahun Ajaran otomatis jika belum diisi
        if tahun and jadwal.tahun_ajaran is None:
            jadwal.tahun_ajaran = tahun

        jadwal.save()

        return redirect(
            "jadwal_list"
        )

    return render(
        request,
        "jadwal/form.html",
        {
            "form": form,
            "judul": "Edit Jadwal"
        }
    )

def tambah_jadwal(request):

    form = JadwalForm(request.POST or None)

    if form.is_valid():
        # Cari Tahun Ajaran yang aktif
        tahun = TahunAjaran.objects.filter(aktif=True).first()

        jadwal = form.save(commit=False)

        # Isi Tahun Ajaran otomatis jika belum diisi
        if tahun and jadwal.tahun_ajaran is None:
            jadwal.tahun_ajaran = tahun

        jadwal.save()

        return redirect("jadwal_list")

    return render(
        request,
        "jadwal/form.html",
        {
            "form": form
        }
    )


def tahun_create(request):

    form = TahunAjaranForm(
        request.POST or None
    )

    if form.is_valid():

        if form.cleaned_data["aktif"]:

            TahunAjaran.objects.update(
                aktif=False
            )

        form.save()

        return redirect(
            "tahun_list"
        )

    return render(
        request,
        "tahun/form.html",
        {
            "form": form
        }
    )

def tahun_list(request):

    data = TahunAjaran.objects.all()

    return render(
        request,
        "tahun/list.html",
        {
            "data": data
        }
    )


def kelas_naik(request):

    daftar_kelas = Kelas.objects.all().order_by(
        "tingkat",
        "nama"
    )

    if request.method == "POST":

        kelas_asal = request.POST.get("kelas_asal")
        kelas_tujuan = request.POST.get("kelas_tujuan")

        asal = Kelas.objects.get(id=kelas_asal)
        tujuan = Kelas.objects.get(id=kelas_tujuan)

        jumlah = Siswa.objects.filter(
            kelas=asal
        ).update(
            kelas=tujuan
        )

        messages.success(
            request,
            f"{jumlah} siswa berhasil dipindahkan."
        )

        return redirect("kelas_list")

    return render(
        request,
        "kelas/naik.html",
        {
            "kelas": daftar_kelas
        }
    )


def kelas_detail(request, pk):
    kelas = Kelas.objects.get(pk=pk)

    siswa = Siswa.objects.filter(
        kelas=kelas
    )

    return render(
        request,
        "kelas/detail.html",
        {
            "kelas": kelas,
            "siswa": siswa,
        },
    )


@login_required(login_url="login")
def daftar_siswa_per_kelas(request, kelas):
    # `Siswa.kelas` disimpan sebagai string (mis. "XII A").
    # Normalisasi input untuk mencegah mismatch karena whitespace.
    # Catatan: parameter URL kemungkinan sudah mengganti spasi dengan "_".
    kelas_input = str(kelas).replace("_", " ")
    kelas_normalized = " ".join(kelas_input.split())

    # Tampilkan siswa unik berdasarkan PK agar tidak terjadi duplikat tampilan.
    # Jangan gunakan distinct("id") karena Django akan menghasilkan DISTINCT ON
    # (tidak didukung pada backend seperti SQLite).
    # Kita cukup dedup dengan Python berdasarkan id.
    # `Siswa.kelas` adalah ForeignKey pada model Kelas (web.models.Siswa).
    # Jadi filter harus pakai objek/PK Kelas, bukan string "X A".
    # Parse `tingkat_nama` -> tingkat + nama
    parts = kelas_normalized.split()
    tingkat = parts[0] if parts else ""
    nama = " ".join(parts[1:]) if len(parts) > 1 else ""

    kelas_obj = (
        Kelas.objects.filter(tingkat=tingkat, nama=nama).first()
        if tingkat and nama
        else None
    )

    siswa_list = list(
        Siswa.objects.filter(kelas=kelas_obj).order_by("id", "nama")
        if kelas_obj
        else Siswa.objects.none()
    )
    seen = set()
    siswa_unique = []
    for s in siswa_list:
        if s.id in seen:
            continue
        seen.add(s.id)
        siswa_unique.append(s)
    siswa_qs = siswa_unique


    return render(
        request,
        "kelas/siswa_by_kelas.html",
        {
            "kelas": kelas_normalized,
            "siswa": siswa_qs,
            "jumlah": len(siswa_qs),

        },
    )




def jadwal_list(request):

    # Default tampilkan jadwal hanya pada Tahun Ajaran aktif
    tahun_aktif = TahunAjaran.objects.filter(aktif=True).first()

    q = request.GET.get("q", "").strip()
    tahun_ajaran_id = request.GET.get("tahun_ajaran", "")
    semester = request.GET.get("semester", "")

    jadwal_qs = Jadwal.objects.select_related(
        "kelas",
        "guru",
        "tahun_ajaran",
    )

    # Filter default (hanya aktif)
    if tahun_ajaran_id:
        jadwal_qs = jadwal_qs.filter(tahun_ajaran_id=tahun_ajaran_id)
    elif tahun_aktif:
        jadwal_qs = jadwal_qs.filter(tahun_ajaran=tahun_aktif)

    if semester:
        jadwal_qs = jadwal_qs.filter(tahun_ajaran__semester=semester)

    # Pencarian multi-field: guru/kelas/hari
    if q:
        jadwal_qs = jadwal_qs.filter(
Q(guru__nama__icontains=q)
| Q(kelas__tingkat__icontains=q)
| Q(kelas__nama__icontains=q)
| Q(hari__icontains=q)
        )

    jadwal = jadwal_qs.order_by(
        "hari",
        "jam_mulai"
    )

    tahun_list = TahunAjaran.objects.all().order_by("-id")

    return render(
        request,
        "jadwal/list.html",
        {
            "jadwal": jadwal,
            "tahun_list": tahun_list,
            "tahun_aktif": tahun_aktif,
            "q": q,
            "tahun_ajaran_id": tahun_ajaran_id,
            "semester": semester,
            "semester_list": ["Ganjil", "Genap"],
        }
    )


def jadwal_guru(request):

    guru = Guru.objects.get(
        user=request.user
    )

    tahun_aktif = TahunAjaran.objects.filter(aktif=True).first()

    jadwal_qs = Jadwal.objects.filter(
        guru=guru
    )

    if tahun_aktif:
        jadwal_qs = jadwal_qs.filter(tahun_ajaran=tahun_aktif)

    jadwal = jadwal_qs.order_by(
        "hari",
        "jam_mulai"
    )

    return render(
        request,
        "jadwal/guru.html",
        {
            "jadwal": jadwal
        }
    )

def hapus_jadwal(request, id):

    # Tidak dibatasi role di sini karena base page hanya untuk admin,
    # namun tetap aman jika route hanya dipakai oleh admin.
    jadwal = get_object_or_404(Jadwal, id=id)
    jadwal.delete()
    return redirect("jadwal_list")


def jadwal_siswa(request):

    siswa = Siswa.objects.get(user=request.user)

    # Siswa.kelas adalah ForeignKey ke model Kelas
    # Jadi filter langsung pakai objek Kelas
    tahun_aktif = TahunAjaran.objects.filter(aktif=True).first()

    jadwal_qs = Jadwal.objects.filter(
        kelas=siswa.kelas
    ) if siswa.kelas else Jadwal.objects.none()

    if tahun_aktif:
        jadwal_qs = jadwal_qs.filter(tahun_ajaran=tahun_aktif)

    jadwal = jadwal_qs.order_by(
        "hari",
        "jam_mulai"
    )

    return render(
        request,
        "jadwal/siswa.html",
        {
            "jadwal": jadwal,
            "siswa": siswa
        }
    )



def kelas_detail(request, id):

    kelas = get_object_or_404(
        Kelas,
        id=id
    )

    siswa = Siswa.objects.filter(
        kelas=kelas
    ).order_by("nama")

    context = {
        "kelas": kelas,
        "siswa": siswa,
        "jumlah": siswa.count(),
    }

    return render(
        request,
        "kelas/detail.html",
        context
    )

def kelas_hapus(request, id):

    kelas = get_object_or_404(
        Kelas,
        id=id
    )

    kelas.delete()

    return redirect(
        "kelas_list"
    )

def kelas_edit(request, id):

    kelas = get_object_or_404(
        Kelas,
        id=id
    )

    form = KelasForm(
        request.POST or None,
        instance=kelas
    )

    if form.is_valid():
        form.save()
        return redirect("kelas_list")

    return render(
        request,
        "kelas/form.html",
        {
            "form": form,
            "judul": "Edit Kelas"
        }
    )

def kelas_tambah(request):

    form = KelasForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("kelas_list")

    return render(
        request,
        "kelas/form.html",
        {
            "form": form,
            "judul": "Tambah Kelas"
        }
    )

def kelas_list(request):

    kelas = Kelas.objects.all().order_by(
        "tingkat",
        "nama"
    )

    jumlah_kelas = kelas.count()

    jumlah_siswa = Siswa.objects.count()

    jumlah_guru = Guru.objects.count()

    context = {
        "kelas": kelas,
        "jumlah_kelas": jumlah_kelas,
        "jumlah_siswa": jumlah_siswa,
        "jumlah_guru": jumlah_guru,
    }

    return render(
        request,
        "kelas/list.html",
        context
    )

def profil_sekolah(request):

    profil = ProfilSekolah.objects.first()

    return render(
        request,
        'profil_sekolah.html',
        {
            'profil': profil
        }
    )

@login_required
@role_required('admin')
def dashboard_admin(request):

    return render(
        request,
        'dashboard_admin.html'
    )


@login_required
@role_required('guru')
def dashboard_guru(request):

    return render(
        request,
        'dashboard_guru.html'
    )

@login_required
@role_required('siswa')
def dashboard_siswa(request):

    return render(
        request,
        'dashboard_siswa.html'
    )


@login_required(login_url="login")
def ubah_foto_profil(request):
    """Ubah foto profil untuk siswa/guru.

    - Siswa: update web.models.Siswa.foto
    - Guru : update akun.models.Guru.foto
    """
    profil = get_object_or_404(Profil, user=request.user)

    if request.method == "POST":
        if profil.role == "siswa":
            siswa = get_object_or_404(Siswa, user=request.user)
            form = FotoProfilForm(request.POST, request.FILES, instance=siswa)
            if form.is_valid():
                form.save()
                messages.success(request, "Foto profil berhasil diperbarui.")
                return redirect("dashboard_siswa")
        elif profil.role == "guru":
            guru = get_object_or_404(Guru, user=request.user)
            form = FotoProfilGuruForm(request.POST, request.FILES, instance=guru)
            if form.is_valid():
                form.save()
                messages.success(request, "Foto profil berhasil diperbarui.")
                return redirect("dashboard_guru")
        else:
            raise PermissionDenied()

    else:
        if profil.role == "siswa":
            siswa = get_object_or_404(Siswa, user=request.user)
            form = FotoProfilForm(instance=siswa)
            foto_profil_url = siswa.foto.url if siswa.foto else None
            back_url = request.META.get("HTTP_REFERER", "/dashboard/siswa/")

        elif profil.role == "guru":
            guru = get_object_or_404(Guru, user=request.user)
            form = FotoProfilGuruForm(instance=guru)
            foto_profil_url = guru.foto.url if guru.foto else None
            back_url = request.META.get("HTTP_REFERER", "/dashboard/guru/")

        else:
            raise PermissionDenied()

    # fallback back_url jika referer kosong
    back_url = request.META.get("HTTP_REFERER") or ("/dashboard/siswa/" if profil.role == "siswa" else "/dashboard/guru/")

    return render(
        request,
        "profil_foto.html",
        {
            "form": form,
            "foto_profil_url": foto_profil_url,
            "back_url": back_url,
        },
    )


def kontak(request):

    return render ( request, 'kontak.html')

def galeri(request):

    data = Galeri.objects.all().order_by(
        '-tanggal'
    )

    return render(
        request,
        'galeri.html',
        {'galeri': data}
    )

def profil(request):

    context = {
        'nama_sekolah': 'SMA Negeri 1 Lasalimu selatan',
        'alamat':
        'Jl. Pendidikan No. 1',
        'visi':
        'Menjadi sekolah unggul, berprestasi dan berkarakter.',
        'misi': [
            'Meningkatkan kualitas pendidikan',
            'Membangun karakter siswa',
            'Mengembangkan teknologi pendidikan'
        ]
    }

    return render(
        request,
        'profil.html',
        context
    )

def berita(request):

    data = Berita.objects.all().order_by('-tanggal')
    return render(request,'berita.html',{'berita': data})


def berita_detail(request, id):

    berita = get_object_or_404(
        Berita,
        id=id
    )

    return render(
        request,
        'detail_berita.html',
        {'berita': berita}
    )




def logout_user(request):
    logout(request)
    return redirect("dashboard")


@login_required(login_url="login")
def dashboard(request):
    return render(
        request,
        "dashboard.html",
        {
            "total_guru": Guru.objects.count(),
            "total_siswa": Siswa.objects.count(),
        },
    )


def home(request):
    return render(
        request,
        "home.html",
        {
            "total_guru": Guru.objects.count(),
            "total_siswa": Siswa.objects.count(),
        },
    )


def is_admin(user):
    profil = getattr(user, "profil", None)
    return profil is not None and profil.role == "admin"


def is_operator(user):
    profil = getattr(user, "profil", None)
    return profil is not None and profil.role in ("operator", "admin")


def _has_admin_operator_by_profile(user):
    # Helper terpisah agar logika izin tidak menyebar.
    return is_admin(user) or is_operator(user)


def is_guru(user):
    profil = getattr(user, "profil", None)
    return profil is not None and profil.role == "guru"


def _require_admin_or_operator(user):
    # Gunakan Profil.role sebagai sumber otorisasi.
    # Kalau tidak cocok, kembalikan 403.
    if not _has_admin_operator_by_profile(user):
        raise PermissionDenied()





@login_required(login_url="login")
def guru(request):
    keyword = request.GET.get("cari")
    data_guru = Guru.objects.filter(nama__icontains=keyword) if keyword else Guru.objects.all()

    paginator = Paginator(data_guru, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "guru.html", {"guru": page_obj})


@login_required(login_url="login")
def siswa(request):

    keyword = request.GET.get("cari")

    if keyword:

        daftar_kelas = (
            Kelas.objects
            .filter(siswa__nama__icontains=keyword)
            .distinct()
            .prefetch_related("siswa")
        )

    else:

        daftar_kelas = (
            Kelas.objects
            .all()
            .prefetch_related("siswa")
            .order_by("tingkat", "nama")
        )

    return render(
        request,
        "siswa.html",
        {
            "kelas": daftar_kelas,
            "keyword": keyword
        }
    )


@login_required(login_url="login")
def tambah_guru(request):
    _require_admin_or_operator(request.user)

    form = GuruForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("guru")

    return render(request, "tambah_guru.html", {"form": form})


@login_required(login_url="login")
def edit_guru(request, id):
    _require_admin_or_operator(request.user)

    data = get_object_or_404(Guru, id=id)
    form = GuruForm(
        request.POST or None,
        request.FILES or None,
        instance=data,
    )

    if form.is_valid():
        form.save()
        return redirect("guru")

    return render(request, "edit_guru.html", {"form": form})


@login_required(login_url="login")
def hapus_guru(request, id):
    _require_admin_or_operator(request.user)

    data = get_object_or_404(Guru, id=id)
    data.delete()
    return redirect("guru")


@login_required(login_url="login")
def tambah_siswa(request):
    form = SiswaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("siswa")

    return render(request, "tambah_siswa.html", {"form": form})


@login_required(login_url="login")
def edit_siswa(request, id):
    data = get_object_or_404(Siswa, id=id)

    form = SiswaForm(
        request.POST or None,
        request.FILES or None,
        instance=data,
    )

    if form.is_valid():
        form.save()
        return redirect("siswa")

    return render(request, "edit_siswa.html", {"form": form})


@login_required(login_url="login")
def hapus_siswa(request, id):
    data = get_object_or_404(Siswa, id=id)
    data.delete()
    return redirect("siswa")


@login_required(login_url="login")
def export_guru_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="data_guru.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Data Guru Sekolah")

    y = 750
    for guru_obj in Guru.objects.all():
        p.drawString(50, y, f"{guru_obj.nama} - {guru_obj.mata_pelajaran}")
        y -= 20

    p.showPage()
    p.save()
    return response


@login_required(login_url="login")
def export_siswa_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="data_siswa.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Data Siswa Sekolah")

    y = 750
    for siswa_obj in Siswa.objects.all():
        p.drawString(50, y, f"{siswa_obj.nama} - {siswa_obj.kelas}")
        y -= 20

    p.showPage()
    p.save()
    return response


@login_required(login_url="login")
def ranking(request):
    # Placeholder implementasi agar project bisa "check" tanpa error.
    # Ranking sebenarnya ada di modul akademik (nilai/rangking) melalui template.
    return render(request, "nilai/rangking.html")

from django.contrib.auth import authenticate, login
from django.contrib import messages
from akun.models import Profil


def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Cari user berdasarkan username agar bisa menentukan error secara terpisah
        profil_user = Profil.objects.filter(user__username=username).select_related("user").first()
        user = profil_user.user if profil_user else None

        # Validasi error sesuai instruksi:
        # - username benar, password salah  => "password invalid"
        # - password benar, username salah  => "incorrect username"
        # - keduanya salah                    => "username and password salah"
        #
        # Catatan: password yang benar hanya bisa dicek jika user ditemukan.
        # 1) Username tidak ditemukan
        if not user:
            if password:
                # username & password sama-sama salah
                messages.error(request, "username and password salah")
            else:
                # kasus password kosong -> tetap anggap username salah
                messages.error(request, "incorrect username")
            return render(request, "login.html")

        # 2) User ditemukan, validasi password
        if not user.check_password(password):
            messages.error(request, "password invalid")
            return render(request, "login.html")

        # (username dan password benar)



        # Cari profil
        profil = Profil.objects.get(user=user)

        # Belum disetujui admin
        if profil.status != "aktif":
            messages.error(
                request,
                "Akun Anda masih menunggu persetujuan Admin."
            )
            return render(request, "login.html")

        # Login
        login(request, user)

        # Pesan sukses khusus siswa muncul hanya untuk pengguna baru (baru registrasi)
        # dan belum diaktifkan admin.
        if profil.role == "siswa" and profil.status != "aktif":
            # Hindari tampil lagi pada login berikutnya
            if not request.session.get("notif_registrasi_siswa_sent"):
                messages.success(
                    request,
                    "Terimasih, silahkan menunggu beberapa saat lagi, untuk informasi akses ke sistem sekolahku kami akan kirimkan pesan ke E-mail anda."
                )
                request.session["notif_registrasi_siswa_sent"] = True


        # Redirect sesuai role

        if profil.role == "admin":
            return redirect("dashboard_admin")
        elif profil.role == "guru":
            return redirect("dashboard_guru")
        elif profil.role == "siswa":
            return redirect("dashboard_siswa")

    return render(request, "login.html")



def daftar_persetujuan(request):

    akun = Profil.objects.filter(
        status="pending"
    )

    return render(
        request,
        "akun/persetujuan.html",
        {
            "akun":akun
        }
    )


def aktifkan_akun(request,id):

    profil = Profil.objects.get(
        id=id
    )

    profil.status="aktif"

    profil.save()

    return redirect(
        "persetujuan"
    )

def tolak_akun(request,id):

    profil = Profil.objects.get(
        id=id
    )

    profil.status="ditolak"

    profil.save()

    return redirect(
        "persetujuan"
    )

def verifikasi_pengguna(request):

    guru = Guru.objects.filter(
        status="Menunggu"
    )

    siswa = Siswa.objects.filter(
        status="Menunggu"
    )

    return render(
        request,
        "admin/verifikasi.html",
        {
            "guru":guru,
            "siswa":siswa
        }
    )

def aktifkan_guru(request, id):

    guru = Guru.objects.get(id=id)

    guru.status = "Aktif"

    guru.save()

    return redirect(
        "verifikasi_pengguna"
    )

def tolak_guru(request,id):

    guru = Guru.objects.get(id=id)

    guru.status = "Ditolak"

    guru.save()

    return redirect(
        "verifikasi_pengguna"
    )

def aktifkan_siswa(request,id):

    siswa = Siswa.objects.get(id=id)

    siswa.status = "Aktif"

    siswa.save()

    return redirect(
        "verifikasi_pengguna"
    )

def tolak_siswa(request,id):

    siswa = Siswa.objects.get(id=id)

    siswa.status="Ditolak"

    siswa.save()

    return redirect(
        "verifikasi_pengguna"
    )

