from django import forms
from .models import Inquiry, Product

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['full_name', 'email', 'phone', 'message', 'product']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom complet',
                'autocomplete': 'name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre.email@domaine.com',
                'autocomplete': 'email',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Téléphone (optionnel)',
                'autocomplete': 'tel'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Votre demande (mesures particulières, tissu, conseil de taille...)',
                'rows': 4,
                'required': 'required'
            }),
            'product': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permettre de laisser product vide si c'est une demande générale
        self.fields['product'].required = False
