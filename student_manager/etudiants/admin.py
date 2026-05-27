# etudiants/admin.py
from django.contrib import admin
from .models import Etudiant


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'prenom', 'nom', 'email', 'a_photo')
    list_filter = ('nom',)
    search_fields = ('matricule', 'nom', 'prenom', 'email')

    def a_photo(self, obj):
        return bool(obj.photo)

    a_photo.boolean = True
    a_photo.short_description = "Photo"