from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):

    ROLE_CHOICES = (
        ("admin","Admin"),
        ("guru","Guru"),
        ("siswa","Siswa"),
    )

    STATUS = (
        ("pending","Menunggu"),
        ("aktif","Aktif"),
        ("ditolak","Ditolak"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    def __str__(self):
        return f"{self.user.username} ({self.status})"