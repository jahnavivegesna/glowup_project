"""
GLOW UP - Views
All page views and API endpoints
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Product, Category, Cart, CartItem, Wishlist,
    Order, OrderItem, Review, Coupon, NewsletterSubscription,
    UserProfile, Offer
)
from .forms import (
    RegistrationForm, LoginForm, CheckoutForm,
    ReviewForm, NewsletterForm, UserUpdateForm, ProfileUpdateForm
)


# ─── Helper: get or create cart for session/user ──────────────────────────────
def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    return None


# ════════════════════════════════════════════════════════════════════════════════
# MAIN PAGES
# ════════════════════════════════════════════════════════════════════════════════

def home(request):
    """Home page with featured products, new arrivals, trending, offers"""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True, is_available=True)[:8]
    trending = Product.objects.filter(is_trending=True, is_available=True)[:6]
    categories = Category.objects.filter(is_active=True)[:6]
    offers = Offer.objects.filter(is_active=True)[:3]
    reviews = Review.objects.select_related('user', 'product').order_by('-created_at')[:6]

    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'trending': trending,
        'categories': categories,
        'offers': offers,
        'reviews': reviews,
        'page_title': 'GLOW UP - Luxury Skincare',
    }
    return render(request, 'store/home.html', context)


def about(request):
    """About page with brand story, mission, testimonials"""
    reviews = Review.objects.select_related('user', 'product').order_by('-created_at')[:6]
    context = {
        'reviews': reviews,
        'page_title': 'About Us - GLOW UP',
    }
    return render(request, 'store/about.html', context)


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        # In production: send actual email
        messages.success(request, "Thank you for reaching out! We'll get back to you within 24 hours.")
        return redirect('contact')

    return render(request, 'store/contact.html', {'page_title': 'Contact Us - GLOW UP'})


# ════════════════════════════════════════════════════════════════════════════════
# PRODUCTS
# ════════════════════════════════════════════════════════════════════════════════

def products(request):
    """Products listing with filters, sorting, pagination"""
    products_qs = Product.objects.filter(is_available=True).select_related('category')

    # ── Filters ──────────────────────────────────────────────────────────────
    category_slug = request.GET.get('category')
    skin_type = request.GET.get('skin_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    sort = request.GET.get('sort', 'newest')
    q = request.GET.get('q', '')

    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)
    if skin_type:
        products_qs = products_qs.filter(skin_type=skin_type)
    if min_price:
        products_qs = products_qs.filter(original_price__gte=min_price)
    if max_price:
        products_qs = products_qs.filter(original_price__lte=max_price)
    if q:
        products_qs = products_qs.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(brand__icontains=q)
        )

    # ── Sorting ──────────────────────────────────────────────────────────────
    sort_options = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'price_low': 'original_price',
        'price_high': '-original_price',
        'name_az': 'name',
        'name_za': '-name',
    }
    products_qs = products_qs.order_by(sort_options.get(sort, '-created_at'))

    # ── Pagination ────────────────────────────────────────────────────────────
    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)
    skin_type_choices = Product.SKIN_TYPE_CHOICES

    context = {
        'products': page_obj,
        'categories': categories,
        'skin_type_choices': skin_type_choices,
        'current_category': category_slug,
        'current_skin_type': skin_type,
        'current_sort': sort,
        'search_query': q,
        'total_count': products_qs.count(),
        'page_title': 'Products - GLOW UP',
    }
    return render(request, 'store/products.html', context)


def products_by_category(request, slug):
    """Products filtered by category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return redirect(f'/products/?category={slug}')


def product_detail(request, slug):
    """Single product detail page"""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.select_related('user').all()
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    # Check if user has this in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        try:
            in_wishlist = request.user.wishlist.products.filter(id=product.id).exists()
        except Exception:
            pass

    # Review form
    review_form = ReviewForm()
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'review_form': review_form,
        'user_review': user_review,
        'page_title': f'{product.name} - GLOW UP',
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    """Search products"""
    q = request.GET.get('q', '')
    products_qs = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q) | Q(brand__icontains=q),
        is_available=True
    ) if q else Product.objects.none()

    return render(request, 'store/search.html', {
        'products': products_qs,
        'query': q,
        'page_title': f'Search: {q} - GLOW UP',
    })


# ════════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════════════

def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save phone to profile
            phone = form.cleaned_data.get('phone')
            if phone:
                user.profile.phone = phone
                user.profile.save()

            login(request, user)
            messages.success(request, f"Welcome to GLOW UP, {user.first_name}! 🌿")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'store/register.html', {
        'form': form,
        'page_title': 'Register - GLOW UP',
    })


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Allow login with email too
        from django.contrib.auth.models import User as AuthUser
        if '@' in username:
            try:
                user_obj = AuthUser.objects.get(email=username)
                username = user_obj.username
            except AuthUser.DoesNotExist:
                pass

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}! ✨")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'store/login.html', {'page_title': 'Login - GLOW UP'})


def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect('home')


# ════════════════════════════════════════════════════════════════════════════════
# CART
# ════════════════════════════════════════════════════════════════════════════════

@login_required
def cart_view(request):
    """View shopping cart"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    shipping_charge = 0 if cart.subtotal >= 499 else 49

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_charge': shipping_charge,
        'total': cart.subtotal + shipping_charge,
        'page_title': 'My Cart - GLOW UP',
    }
    return render(request, 'store/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to cart"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Cart updated — {product.name} quantity increased!")
        else:
            messages.warning(request, f"Sorry, only {product.stock} units available.")
    else:
        messages.success(request, f"✨ {product.name} added to your cart!")

    # If AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f'{product.name} added to cart!'
        })

    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from cart.")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = request.user.cart
        return JsonResponse({'success': True, 'cart_count': cart.total_items})

    return redirect('cart')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    elif quantity > cart_item.product.stock:
        messages.warning(request, f"Only {cart_item.product.stock} units available.")
        cart_item.quantity = cart_item.product.stock
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = request.user.cart
        return JsonResponse({
            'success': True,
            'item_total': float(cart_item.total_price),
            'cart_subtotal': float(cart.subtotal),
            'cart_count': cart.total_items,
        })

    return redirect('cart')


@login_required
def clear_cart(request):
    """Clear all items from cart"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    messages.success(request, "Cart cleared.")
    return redirect('cart')


# ════════════════════════════════════════════════════════════════════════════════
# WISHLIST
# ════════════════════════════════════════════════════════════════════════════════

@login_required
def toggle_wishlist(request, product_id):
    """Add or remove product from wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    if wishlist.products.filter(id=product_id).exists():
        wishlist.products.remove(product)
        action = 'removed'
        msg = f"{product.name} removed from wishlist."
    else:
        wishlist.products.add(product)
        action = 'added'
        msg = f"💖 {product.name} added to wishlist!"

    messages.success(request, msg)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'action': action,
            'wishlist_count': wishlist.products.count()
        })

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def wishlist_view(request):
    """View wishlist"""
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products_qs = wishlist.products.filter(is_available=True)
    return render(request, 'store/wishlist.html', {
        'wishlist_products': products_qs,
        'page_title': 'My Wishlist - GLOW UP',
    })


# ════════════════════════════════════════════════════════════════════════════════
# CHECKOUT & ORDERS
# ════════════════════════════════════════════════════════════════════════════════

@login_required
def apply_coupon(request):
    """Apply coupon code via AJAX"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        try:
            coupon = Coupon.objects.get(code=code)
            if not coupon.is_valid():
                return JsonResponse({'success': False, 'message': 'This coupon has expired or is invalid.'})

            cart = request.user.cart
            if cart.subtotal < coupon.min_order_amount:
                return JsonResponse({
                    'success': False,
                    'message': f'Minimum order of ₹{coupon.min_order_amount} required for this coupon.'
                })

            discount = coupon.calculate_discount(cart.subtotal)
            request.session['coupon_id'] = coupon.id
            request.session['discount'] = float(discount)

            return JsonResponse({
                'success': True,
                'message': f'🎉 Coupon applied! You save ₹{discount:.2f}',
                'discount': float(discount),
                'coupon_code': coupon.code,
            })
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})


@login_required
def checkout(request):
    """Checkout page"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()

    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('products')

    # Pre-fill with user profile data
    profile = request.user.profile
    initial_data = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'phone': profile.phone,
        'address_line1': profile.address_line1,
        'address_line2': profile.address_line2,
        'city': profile.city,
        'state': profile.state,
        'pincode': profile.pincode,
    }

    # Coupon from session
    coupon = None
    discount = 0
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            discount = float(request.session.get('discount', 0))
        except Coupon.DoesNotExist:
            pass

    shipping_charge = 0 if cart.subtotal >= 499 else 49
    total = float(cart.subtotal) + shipping_charge - discount

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Create Order
            order = Order.objects.create(
                user=request.user,
                coupon=coupon,
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                address_line1=data['address_line1'],
                address_line2=data.get('address_line2', ''),
                city=data['city'],
                state=data['state'],
                pincode=data['pincode'],
                subtotal=cart.subtotal,
                discount_amount=discount,
                shipping_charge=shipping_charge,
                total=total,
                payment_method='cod',
                status='confirmed',
            )

            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                    total_price=item.total_price,
                )
                # Reduce stock
                item.product.stock -= item.quantity
                item.product.save()

            # Update coupon usage
            if coupon:
                coupon.used_count += 1
                coupon.save()
                del request.session['coupon_id']
                if 'discount' in request.session:
                    del request.session['discount']

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f"🎉 Order #{order.order_id} placed successfully!")
            return redirect('order_success', order_id=order.order_id)
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': cart.subtotal,
        'discount': discount,
        'shipping_charge': shipping_charge,
        'total': total,
        'coupon': coupon,
        'page_title': 'Checkout - GLOW UP',
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {
        'order': order,
        'page_title': f'Order Confirmed - GLOW UP',
    })


# ════════════════════════════════════════════════════════════════════════════════
# USER DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════

@login_required
def dashboard(request):
    """User dashboard - overview"""
    orders = request.user.orders.all()[:5]
    wishlist_count = 0
    try:
        wishlist_count = request.user.wishlist.products.count()
    except Exception:
        pass

    new_arrivals = Product.objects.filter(is_new_arrival=True, is_available=True)[:4]
    offers = Offer.objects.filter(is_active=True)[:3]
    coupons = Coupon.objects.filter(is_active=True, valid_until__gte=timezone.now())[:5]

    context = {
        'orders': orders,
        'wishlist_count': wishlist_count,
        'total_orders': request.user.orders.count(),
        'new_arrivals': new_arrivals,
        'offers': offers,
        'coupons': coupons,
        'page_title': 'My Dashboard - GLOW UP',
    }
    return render(request, 'store/dashboard.html', context)


@login_required
def profile_update(request):
    """Update user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully! ✨")
            return redirect('profile_update')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'store/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'Edit Profile - GLOW UP',
    })


@login_required
def order_history(request):
    """All user orders"""
    orders = request.user.orders.prefetch_related('items').all()
    paginator = Paginator(orders, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'store/order_history.html', {
        'orders': page_obj,
        'page_title': 'Order History - GLOW UP',
    })


@login_required
def order_detail(request, order_id):
    """Single order detail"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {
        'order': order,
        'page_title': f'Order #{order.order_id} - GLOW UP',
    })


@login_required
def coupons_view(request):
    """Available coupons for user"""
    coupons = Coupon.objects.filter(is_active=True, valid_until__gte=timezone.now())
    return render(request, 'store/coupons.html', {
        'coupons': coupons,
        'page_title': 'My Coupons - GLOW UP',
    })


# ════════════════════════════════════════════════════════════════════════════════
# REVIEWS
# ════════════════════════════════════════════════════════════════════════════════

@login_required
def add_review(request, slug):
    """Add a review for a product"""
    product = get_object_or_404(Product, slug=slug)

    # Check if user already reviewed
    existing = Review.objects.filter(product=product, user=request.user).first()
    if existing:
        messages.warning(request, "You've already reviewed this product.")
        return redirect('product_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review! 💫")
        else:
            messages.error(request, "Please fix the form errors.")

    return redirect('product_detail', slug=slug)


# ════════════════════════════════════════════════════════════════════════════════
# NEWSLETTER
# ════════════════════════════════════════════════════════════════════════════════

def newsletter_subscribe(request):
    """Subscribe to newsletter"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            sub, created = NewsletterSubscription.objects.get_or_create(email=email)
            if created:
                messages.success(request, "🌿 You're subscribed! Watch your inbox for exclusive offers.")
            else:
                messages.info(request, "You're already subscribed. Thank you!")
        else:
            messages.error(request, "Please enter a valid email address.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))

from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

def load_data_view(request):
    from django.core.management import call_command
    from django.contrib.auth.models import User
    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@gmail.com', 'admin1234')
    # Load sample data
    call_command('load_sample_data')
    return HttpResponse("Done! Admin created and sample data loaded!")