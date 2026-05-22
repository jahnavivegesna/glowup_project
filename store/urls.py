"""GLOW UP - URL Patterns"""

from django.urls import path
from . import views

urlpatterns = [
    # ─── Main Pages ──────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ─── Products ────────────────────────────────────────────────────────────
    path('products/', views.products, name='products'),
    path('products/category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),

    # ─── Authentication ───────────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ─── Dashboard ────────────────────────────────────────────────────────────
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile_update, name='profile_update'),
    path('dashboard/orders/', views.order_history, name='order_history'),
    path('dashboard/orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('dashboard/wishlist/', views.wishlist_view, name='wishlist'),
    path('dashboard/coupons/', views.coupons_view, name='coupons'),

    # ─── Cart ─────────────────────────────────────────────────────────────────
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # ─── Wishlist ─────────────────────────────────────────────────────────────
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # ─── Checkout & Orders ────────────────────────────────────────────────────
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<str:order_id>/', views.order_success, name='order_success'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

    # ─── Reviews ──────────────────────────────────────────────────────────────
    path('product/<slug:slug>/review/', views.add_review, name='add_review'),

    # ─── Newsletter ───────────────────────────────────────────────────────────
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Load data
    path('load-data/', views.load_data_view, name='load_data'),
]
