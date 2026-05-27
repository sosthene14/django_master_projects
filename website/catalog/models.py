from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la collection")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description poétique")
    image_path = models.CharField(max_length=255, verbose_name="Chemin de l'image (statique)")
    is_active = models.BooleanField(default=True, verbose_name="Est active")

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Collection")
    name = models.CharField(max_length=200, verbose_name="Nom de la pièce")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description du produit")
    details = models.TextField(verbose_name="Matières & Entretien", help_text="Séparez les lignes par des sauts de ligne")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Prix (FCFA)")
    image_path = models.CharField(max_length=255, verbose_name="Chemin de l'image (statique)")
    is_featured = models.BooleanField(default=False, verbose_name="Mise en avant (accueil)")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Pièce de mode"
        verbose_name_plural = "Pièces de mode"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_details_list(self):
        """Retourne les lignes de détails sous forme de liste pour l'affichage."""
        return [line.strip() for line in self.details.split('\n') if line.strip()]

class Inquiry(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='inquiries', verbose_name="Pièce concernée")
    message = models.TextField(verbose_name="Message / Demande")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")

    class Meta:
        verbose_name = "Demande d'information"
        verbose_name_plural = "Demandes d'information"
        ordering = ['-created_at']

    def __str__(self):
        return f"Demande de {self.full_name} ({self.email})"
