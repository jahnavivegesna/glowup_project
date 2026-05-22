"""
GLOW UP - Admin Configuration
Professional admin panel setup
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, Review, Cart, CartItem,
    Wishlist, Order, OrderItem, Coupon,
    NewsletterSubscription, UserProfile, Offer
)


# ─── Category Admin ────────────────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


# ─── Product Admin ─────────────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'product_image', 'name', 'category', 'brand', 'original_price',
        'discount_price', 'stock', 'is_available', 'is_featured',
        'is_new_arrival', 'is_trending', 'created_at'
    ]
    list_filter = ['category', 'is_available', 'is_featured', 'is_new_arrival', 'skin_type']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_available', 'is_featured', 'is_new_arrival', 'is_trending', 'stock']
    readonly_fields = ['discount_percent', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'name', 'slug', 'brand', 'skin_type', 'weight', 'tags')
        }),
        ('Description', {
            'fields': ('description', 'ingredients', 'how_to_use')
        }),
        ('Pricing', {
            'fields': ('original_price', 'discount_price', 'discount_percent')
        }),
        ('Images', {
            'fields': ('image', 'image2', 'image3')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_available')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_new_arrival', 'is_trending')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def product_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:8px;" />', obj.image.url)
        return "No Image"
    product_image.short_description = 'Image'


# ─── Review Admin ──────────────────────────────────────────────────────────────
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'title', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified']
    search_fields = ['user__username', 'product__name']
    list_editable = ['is_verified']


# ─── Order Admin ───────────────────────────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 'user', 'full_name', 'total', 'status',
        'payment_method', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_id', 'user__username', 'full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {
            'fields': ('order_id', 'user', 'status', 'payment_method', 'coupon')
        }),
        ('Shipping Details', {
            'fields': ('full_name', 'email', 'phone', 'address_line1',
                       'address_line2', 'city', 'state', 'pincode')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'discount_amount', 'shipping_charge', 'total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'delivered_at')
        }),
    )


# ─── Coupon Admin ──────────────────────────────────────────────────────────────
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_type', 'discount_value', 'min_order_amount',
        'used_count', 'max_uses', 'valid_until', 'is_active'
    ]
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code']
    list_editable = ['is_active']


# ─── Newsletter Admin ──────────────────────────────────────────────────────────
@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['email', 'name']
    list_editable = ['is_active']


# ─── User Profile Admin ────────────────────────────────────────────────────────
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'skin_type']
    search_fields = ['user__username', 'user__email', 'phone']


# ─── Offer Admin ───────────────────────────────────────────────────────────────
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percent', 'valid_until', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']


# ─── Cart Admin (read-only) ────────────────────────────────────────────────────
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'updated_at']
    readonly_fields = ['user', 'created_at', 'updated_at']
