from django.db import migrations, models


def convert_data(apps, schema_editor):
    Siswa = apps.get_model("web", "Siswa")
    Kelas = apps.get_model("web", "Kelas")

    for siswa in Siswa.objects.all():

        if not siswa.kelas:
            continue

        try:
            teks = siswa.kelas.strip()

            bagian = teks.split()

            tingkat = bagian[0]
            nama = bagian[1]
            jurusan = bagian[2]

            kelas = Kelas.objects.get(
                tingkat=tingkat,
                nama=nama,
                jurusan=jurusan
            )

            siswa.kelas_id = kelas.id
            siswa.save()

        except Exception:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0014_guru_nip"),
    ]

    operations = [

        migrations.RenameField(
            model_name="siswa",
            old_name="kelas",
            new_name="kelas_lama",
        ),

        migrations.AddField(
            model_name="siswa",
            name="kelas",
            field=models.ForeignKey(
                to="web.kelas",
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
            ),
        ),

        migrations.RunPython(convert_data),

        migrations.RemoveField(
            model_name="siswa",
            name="kelas_lama",
        ),
    ]