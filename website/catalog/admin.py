from django.contrib import admin
from .models import Category, Product, Inquiry

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'is_available', 'created_at')
    list_filter = ('category', 'is_featured', 'is_available', 'created_at')
    search_fields = ('name', 'description', 'details')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_featured', 'is_available')
    ordering = ('-created_at',)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'product', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('full_name', 'email', 'phone', 'product', 'message', 'created_at')
    
    # Empêcher l'ajout manuel de demandes via l'admin pour plus de cohérence
    def has_add_permission(self, request):
        return False
