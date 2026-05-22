"""
GLOW UP - Context Processors
Makes cart count and wishlist count available in ALL templates
"""


def cart_count(request):
    """Add cart item count to every template context"""
    count = 0
    if request.user.is_authenticated:
        try:
            count = request.user.cart.total_items
        except Exception:
            count = 0
    return {'cart_count': count}


def wishlist_count(request):
    """Add wishlist item count to every template context"""
    count = 0
    if request.user.is_authenticated:
        try:
            count = request.user.wishlist.products.count()
        except Exception:
            count = 0
    return {'wishlist_count': count}
