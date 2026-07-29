from django.contrib.auth.models import User
from .forms import RegisterGuruForm, RegisterSiswaForm
from .models import Profil
from web.models import Guru, Siswa
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from akun.forms_foto_profil import FotoProfilGuruForm


@login_required
def aktifkan_akun(request, id):


    print("=" * 40)
    print("ID Profil :", id)


    profil = get_object_or_404(Profil,id=id)

    print("Username :", profil.user.username)
    print("Status sebelum :", profil.status)


    profil.status = "aktif"
    profil.save()

    # Jika tabel lain masih menyimpan status pada model Guru/Siswa,
    # sinkronkan agar konsisten dengan Profil.status.
    try:
        if profil.role == "guru":
            Guru.objects.filter(user=profil.user).update(status="Aktif")
        elif profil.role == "siswa":
            Siswa.objects.filter(user=profil.user).update(status="Aktif")
    except Exception:
        pass



    profil.refresh_from_db()

    print("Status sesudah :", profil.status)
    print("=" * 40)

    return redirect("verifikasi_pengguna")


@login_required
def tolak_akun(request, id):

    profil = get_object_or_404(
        Profil,
        id=id
    )

    profil.status = "ditolak"
    profil.save()

    # Sinkronkan juga status pada model Guru/Siswa (jika ada data lama)
    try:
        if profil.role == "guru":
            Guru.objects.filter(user=profil.user).update(status="Ditolak")
        elif profil.role == "siswa":
            Siswa.objects.filter(user=profil.user).update(status="Ditolak")
    except Exception:
        pass

    return redirect("verifikasi_pengguna")



@login_required
def daftar_persetujuan(request):

    cari = request.GET.get("cari")

    status = request.GET.get("status")

    queryset = Profil.objects.select_related("user")

    if cari:

        queryset = queryset.filter(

            Q(user__username__icontains=cari) |

            Q(user__first_name__icontains=cari)

        )

    if status:

        queryset = queryset.filter(status=status)

    total_pending = Profil.objects.filter(status="pending").count()

    total_aktif = Profil.objects.filter(status="aktif").count()

    total_ditolak = Profil.objects.filter(status="ditolak").count()

    guru = queryset.filter(role="guru")

    siswa = queryset.filter(role="siswa")

    return render(

        request,

        "admin/verifikasi.html",

        {

            "guru": guru,

            "siswa": siswa,

            "total_pending": total_pending,

            "total_aktif": total_aktif,

            "total_ditolak": total_ditolak,

            "cari": cari,

            "status": status,

        }

    )


def register_guru(request):


    form = RegisterGuruForm(request.POST or None)

    if form.is_valid():

        user = form.save(commit=False)

        user.set_password(form.cleaned_data["password"])

        user.save()

        Profil.objects.create(
            user=user,
            role="guru",
            status="pending"
        )

        nip = form.cleaned_data.get("nip")
        mata_pelajaran = form.cleaned_data.get("mata_pelajaran")

        Guru.objects.create(
            user=user,
            nama=user.first_name,
            nip=nip,
            mata_pelajaran=mata_pelajaran,
            email=user.email,
            status="Menunggu"
        )




        from django.contrib import messages
        messages.success(request, "Registrasi berhasil. Silahkan login.")
        return redirect("login")



    return render(
        request,
        "akun/register_guru.html",
        {
            "form": form
        }
    )


def register_siswa(request):

    form = RegisterSiswaForm(request.POST or None)

    if form.is_valid():

        user = form.save(commit=False)

        user.set_password(form.cleaned_data["password"])

        user.save()

        Profil.objects.create(
            user=user,
            role="siswa",
            status="pending"
        )

        nis = form.cleaned_data.get("nis")
        kelas_obj = form.cleaned_data.get("kelas")
        nama_kelas = None
        if kelas_obj:
            # Simpan sebagai string "{tingkat} {nama}"
            nama_kelas = f"{kelas_obj.tingkat} {kelas_obj.nama}"

        Siswa.objects.create(
            user=user,
            nama=user.first_name,
            nis=nis,
            kelas=nama_kelas,
            status="Menunggu"
        )

        from django.contrib import messages
        messages.success(request, "Registrasi berhasil. Silahkan Login.")
        return redirect("login")


    return render(

        request,
        "akun/register_siswa.html",
        {
            "form": form
        }
    )