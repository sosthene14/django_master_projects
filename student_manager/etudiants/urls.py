# etudiants/urls.py
from django.urls import path
from . import views

app_name = 'etudiants'

urlpatterns = [
    path('', views.liste_etudiants, name='liste_etudiants'),
    path('ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('<int:id>/', views.details_etudiant, name='details_etudiant'),
    path('<int:id>/modifier/', views.modifier_etudiant, name='modifier_etudiant'),
    path('<int:id>/supprimer/', views.supprimer_etudiant, name='supprimer_etudiant'),
]