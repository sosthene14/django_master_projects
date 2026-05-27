# etudiants/models.py
from django.db import models
import random
from datetime import datetime


class Etudiant(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    email = models.EmailField(unique=True, verbose_name="Email")
    photo = models.ImageField(
        upload_to='photos_etudiants/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def save(self, *args, **kwargs):
        if not self.matricule:
            year = datetime.now().year
            initials = (self.prenom[:1] if self.prenom else 'X').upper() + (self.nom[:1] if self.nom else 'X').upper()
            for _ in range(10):
                candidate = f"{initials}{year}{random.randint(0, 9999):04d}"
                if not Etudiant.objects.filter(matricule=candidate).exists():
                    self.matricule = candidate
                    break
            else:
                
                self.matricule = f"{initials}{int(datetime.now().timestamp())}"

        super().save(*args, **kwargs)