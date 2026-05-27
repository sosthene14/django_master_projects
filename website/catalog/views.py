from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Category, Product, Inquiry
from .forms import InquiryForm

def home(request):
    categories = Category.objects.filter(is_active=True)[:3]
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:4]
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'title': 'Maison de Haute Couture Minimaliste'
    }
    return render(request, 'catalog/home.html', context)

def product_list(request, category_slug=None):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=selected_category)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'title': f'Collection {selected_category.name}' if selected_category else 'Toutes nos Créations'
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    form = InquiryForm(initial={'product': product})
    
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:3]

    context = {
        'product': product,
        'form': form,
        'related_products': related_products,
        'title': product.name
    }
    return render(request, 'catalog/product_detail.html', context)

def about(request):
    context = {
        'title': 'Notre Philosophie'
    }
    return render(request, 'catalog/about.html', context)

def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Votre message a bien été transmis à notre atelier. Nous vous répondrons avec le plus grand soin sous 24h."
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})
                
            messages.success(request, msg)
            return redirect('catalog:contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': "Veuillez corriger les erreurs dans le formulaire."})
    else:
        form = InquiryForm()

    context = {
        'form': form,
        'title': 'Nous Contacter'
    }
    return render(request, 'catalog/contact.html', context)

def inquiry_submit(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            if inquiry.product:
                msg = f"Votre demande pour la pièce '{inquiry.product.name}' a été transmise à notre atelier. Un conseiller vous contactera sous 24h."
            else:
                msg = "Votre message a été enregistré avec succès."
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})
            
            messages.success(request, msg)
            if inquiry.product:
                return redirect('catalog:product_detail', slug=inquiry.product.slug)
            return redirect('catalog:home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': "Formulaire invalide. Veuillez vérifier vos informations."})
            
            product_id = request.POST.get('product')
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                messages.error(request, "Une erreur est survenue lors de la soumission de votre demande.")
                return redirect('catalog:product_detail', slug=product.slug)
            
            messages.error(request, "Formulaire invalide.")
            return redirect('catalog:home')
            
    return redirect('catalog:home')
