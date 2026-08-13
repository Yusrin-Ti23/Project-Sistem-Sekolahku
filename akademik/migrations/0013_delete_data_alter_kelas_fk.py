from django.db import migrations, models
import django.db.models.deletion


def delete_existing_data(apps, schema_editor):
    Tugas = apps.get_model('akademik', 'Tugas')
    Ujian = apps.get_model('akademik', 'Ujian')
    Materi = apps.get_model('akademik', 'Materi')
    Tugas.objects.all().delete()
    Ujian.objects.all().delete()
    Materi.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('akademik', '0012_absensi_tahun_ajaran_materi_tahun_ajaran_and_more'),
        ('web', '0016_alter_siswa_kelas'),
    ]

    operations = [
        migrations.RunPython(delete_existing_data, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='materi',
            name='kelas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.kelas'),
        ),
        migrations.AlterField(
            model_name='tugas',
            name='kelas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.kelas'),
        ),
        migrations.AlterField(
            model_name='ujian',
            name='kelas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.kelas'),
        ),
    ]
