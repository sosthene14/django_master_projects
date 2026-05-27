# etudiants/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import Etudiant
from .forms import EtudiantForm


def liste_etudiants(request):
    """Affiche la liste de tous les étudiants"""
    query = request.GET.get('q', '').strip()
    matricule = request.GET.get('matricule', '').strip()

    etudiants = Etudiant.objects.all()
    if query:
        etudiants = etudiants.filter(
            Q(nom__icontains=query) | Q(prenom__icontains=query)
        )
    if matricule:
        etudiants = etudiants.filter(matricule__icontains=matricule)

    context = {
        'etudiants': etudiants,
        'q': query,
        'matricule': matricule,
    }
    return render(request, 'etudiants/liste_etudiants.html', context)


def details_etudiant(request, id):
    """Affiche les détails d'un étudiant spécifique"""
    etudiant = get_object_or_404(Etudiant, id=id)
    return render(request, 'etudiants/details_etudiant.html', {'etudiant': etudiant})


def ajouter_etudiant(request):
    """Ajoute un nouvel étudiant"""
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f"L'étudiant {form.cleaned_data['prenom']} {form.cleaned_data['nom']} a été ajouté avec succès!")
            return redirect('etudiants:liste_etudiants')
    else:
        form = EtudiantForm()

    return render(request, 'etudiants/formulaire_etudiant.html', {
        'form': form,
        'titre': 'Ajouter un étudiant'
    })


def modifier_etudiant(request, id):
    """Modifie un étudiant existant"""
    etudiant = get_object_or_404(Etudiant, id=id)

    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'étudiant {etudiant.prenom} {etudiant.nom} a été modifié avec succès!")
            return redirect('etudiants:liste_etudiants')
    else:
        form = EtudiantForm(instance=etudiant)

    return render(request, 'etudiants/formulaire_etudiant.html', {
        'form': form,
        'titre': 'Modifier un étudiant',
        'etudiant': etudiant
    })


def supprimer_etudiant(request, id):
    """Supprime un étudiant"""
    etudiant = get_object_or_404(Etudiant, id=id)

    if request.method == 'POST':
        nom_complet = f"{etudiant.prenom} {etudiant.nom}"
        etudiant.delete()
        messages.success(request, f"L'étudiant {nom_complet} a été supprimé avec succès!")
        return redirect('etudiants:liste_etudiants')

    return render(request, 'etudiants/confirmation_suppression.html', {'etudiant': etudiant})