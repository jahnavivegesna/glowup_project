"""
GLOW UP - Management Command: load_sample_data
Run: python manage.py load_sample_data
Creates sample categories, products, coupons, and offers for demo
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from store.models import Category, Product, Coupon, Offer


class Command(BaseCommand):
    help = 'Load sample data for GLOW UP skincare store'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('🌿 Loading GLOW UP sample data...'))

        # ── Categories ────────────────────────────────────────────────────────
        categories_data = [
            {'name': 'Moisturizers',   'slug': 'moisturizers',   'description': 'Hydrating creams and lotions for all skin types'},
            {'name': 'Cleansers',      'slug': 'cleansers',      'description': 'Gentle face washes and cleansing balms'},
            {'name': 'Serums',         'slug': 'serums',         'description': 'Targeted treatments for specific skin concerns'},
            {'name': 'Sunscreen',      'slug': 'sunscreen',      'description': 'SPF protection for everyday use'},
            {'name': 'Eye Care',       'slug': 'eye-care',       'description': 'Creams and serums for the delicate eye area'},
            {'name': 'Face Masks',     'slug': 'face-masks',     'description': 'Weekly treatments for deep nourishment'},
            {'name': 'Toners',         'slug': 'toners',         'description': 'Balancing and hydrating toners'},
            {'name': 'Lip Care',       'slug': 'lip-care',       'description': 'Nourishing balms and treatments for lips'},
        ]

        cats = {}
        for c in categories_data:
            obj, created = Category.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'description': c['description'], 'is_active': True}
            )
            cats[c['slug']] = obj
            if created:
                self.stdout.write(f'  ✓ Category: {obj.name}')

        # ── Products ──────────────────────────────────────────────────────────
        products_data = [
            # Moisturizers
            {
                'name': 'Hyaluronic Acid Moisture Surge',
                'slug': 'hyaluronic-acid-moisture-surge',
                'category': 'moisturizers',
                'brand': 'GLOW UP',
                'description': 'A lightweight, oil-free moisturizer infused with hyaluronic acid that provides intense 72-hour hydration. Suitable for all skin types, this gel-cream formula absorbs instantly without leaving any greasy residue.',
                'ingredients': 'Aqua, Hyaluronic Acid (3 molecular weights), Niacinamide, Ceramides, Aloe Vera Extract, Vitamin E, Panthenol, Allantoin, Glycerin',
                'how_to_use': 'Apply morning and evening after cleansing and toning. Gently massage 2-3 pumps onto face and neck in upward circular motions. Follow with SPF in the morning.',
                'skin_type': 'all',
                'original_price': 999,
                'discount_price': 799,
                'stock': 50,
                'weight': '50ml',
                'is_featured': True,
                'is_new_arrival': True,
                'is_trending': True,
                'tags': 'hydration, hyaluronic acid, lightweight',
            },
            {
                'name': 'Rich Shea Butter Night Cream',
                'slug': 'rich-shea-butter-night-cream',
                'category': 'moisturizers',
                'brand': 'GLOW UP',
                'description': 'Luxuriously rich overnight cream with shea butter and rosehip oil that repairs and nourishes skin while you sleep. Wake up to plumper, softer, visibly younger-looking skin.',
                'ingredients': 'Shea Butter, Rosehip Oil, Retinol (0.1%), Peptides, Vitamin C, Jojoba Oil, Squalane, Evening Primrose Oil',
                'how_to_use': 'Apply generously to clean face and neck every night. Use 2-3 pea-sized amounts and pat gently until absorbed.',
                'skin_type': 'dry',
                'original_price': 1299,
                'discount_price': 999,
                'stock': 30,
                'weight': '60g',
                'is_featured': True,
                'tags': 'night cream, shea butter, anti-aging',
            },
            # Cleansers
            {
                'name': 'Gentle Micellar Foam Cleanser',
                'slug': 'gentle-micellar-foam-cleanser',
                'category': 'cleansers',
                'brand': 'GLOW UP',
                'description': 'A soap-free, pH-balanced foaming cleanser that removes makeup, dirt, and impurities without stripping the skin\'s natural moisture barrier. Dermatologist-tested for sensitive skin.',
                'ingredients': 'Micellar Water, Aloe Vera, Cucumber Extract, Chamomile, Green Tea Extract, Panthenol, Glycerin',
                'how_to_use': 'Pump 1-2 times onto wet hands, work into a lather, massage onto face for 60 seconds, rinse thoroughly. Use morning and evening.',
                'skin_type': 'sensitive',
                'original_price': 699,
                'discount_price': 549,
                'stock': 60,
                'weight': '150ml',
                'is_featured': True,
                'is_trending': True,
                'tags': 'cleanser, sensitive skin, gentle',
            },
            {
                'name': 'Salicylic Acid Pore Cleanser',
                'slug': 'salicylic-acid-pore-cleanser',
                'category': 'cleansers',
                'brand': 'GLOW UP',
                'description': 'A targeted cleanser with 2% salicylic acid that deeply unclogs pores, controls excess oil, and prevents breakouts. Perfect for acne-prone and oily skin types.',
                'ingredients': 'Salicylic Acid 2%, Tea Tree Oil, Niacinamide, Zinc, Witch Hazel, Green Tea',
                'how_to_use': 'Use on oily or acne-prone areas morning and evening. Avoid eye area. Start with once daily if new to salicylic acid.',
                'skin_type': 'oily',
                'original_price': 799,
                'discount_price': None,
                'stock': 45,
                'weight': '100ml',
                'is_new_arrival': True,
                'tags': 'salicylic acid, acne, pores, oily skin',
            },
            # Serums
            {
                'name': 'Vitamin C Brightening Serum',
                'slug': 'vitamin-c-brightening-serum',
                'category': 'serums',
                'brand': 'GLOW UP',
                'description': 'A powerful 15% stabilized Vitamin C serum that fades dark spots, brightens complexion, and protects against environmental damage. Formulated with ferulic acid for enhanced stability and potency.',
                'ingredients': 'Ascorbic Acid 15%, Ferulic Acid, Vitamin E, Hyaluronic Acid, Niacinamide, Kojic Acid, Turmeric Extract',
                'how_to_use': 'Apply 3-4 drops to clean face every morning before moisturizer. Store in a cool, dark place. Use within 3 months of opening.',
                'skin_type': 'all',
                'original_price': 1499,
                'discount_price': 1199,
                'stock': 35,
                'weight': '30ml',
                'is_featured': True,
                'is_trending': True,
                'tags': 'vitamin c, brightening, dark spots, glow',
            },
            {
                'name': 'Retinol Renewal Night Serum',
                'slug': 'retinol-renewal-night-serum',
                'category': 'serums',
                'brand': 'GLOW UP',
                'description': 'An advanced anti-aging serum with 0.5% encapsulated retinol that reduces fine lines, wrinkles, and uneven texture. Gentle enough for beginners, effective enough for retinol veterans.',
                'ingredients': 'Retinol 0.5% (encapsulated), Bakuchiol, Peptides, Ceramides, Niacinamide, Squalane',
                'how_to_use': 'Apply 4-5 drops on clean face at night, 2-3 times per week. Build up gradually. Always use SPF next morning.',
                'skin_type': 'normal',
                'original_price': 1799,
                'discount_price': 1499,
                'stock': 25,
                'weight': '30ml',
                'is_featured': True,
                'is_new_arrival': True,
                'tags': 'retinol, anti-aging, wrinkles, night serum',
            },
            {
                'name': 'Niacinamide 10% + Zinc Serum',
                'slug': 'niacinamide-10-zinc-serum',
                'category': 'serums',
                'brand': 'GLOW UP',
                'description': 'A high-strength 10% niacinamide serum with 1% zinc that minimises pores, balances oil production, and reduces blemishes. A cult favourite for oily and combination skin.',
                'ingredients': 'Niacinamide 10%, Zinc 1%, Hyaluronic Acid, Panthenol, Tamarind Seed Extract',
                'how_to_use': 'Apply 3-4 drops morning and evening after cleansing. Can be layered under moisturizer.',
                'skin_type': 'combination',
                'original_price': 899,
                'discount_price': 699,
                'stock': 70,
                'weight': '30ml',
                'is_featured': True,
                'is_trending': True,
                'tags': 'niacinamide, zinc, pores, oily skin',
            },
            # Sunscreen
            {
                'name': 'SPF 50+ Invisible Sunscreen',
                'slug': 'spf-50-invisible-sunscreen',
                'category': 'sunscreen',
                'brand': 'GLOW UP',
                'description': 'A lightweight, non-greasy broad-spectrum SPF 50+ sunscreen that leaves absolutely no white cast. PA++++ rating protects against UVA/UVB rays. Suitable for all skin tones.',
                'ingredients': 'Avobenzone 3%, Octisalate, Octocrylene, Titanium Dioxide, Niacinamide, Hyaluronic Acid',
                'how_to_use': 'Apply generously as last step of morning skincare. Reapply every 2-3 hours when outdoors.',
                'skin_type': 'all',
                'original_price': 899,
                'discount_price': 749,
                'stock': 80,
                'weight': '50ml',
                'is_featured': True,
                'is_new_arrival': True,
                'tags': 'sunscreen, spf50, no white cast, UV protection',
            },
            # Eye Care
            {
                'name': 'Caffeine Eye Rescue Cream',
                'slug': 'caffeine-eye-rescue-cream',
                'category': 'eye-care',
                'brand': 'GLOW UP',
                'description': 'A cooling eye cream with 5% caffeine that instantly de-puffs under-eyes, reduces dark circles, and firms the delicate eye area. Ophthalmologist tested.',
                'ingredients': 'Caffeine 5%, Peptides, Vitamin K, Hyaluronic Acid, Aloe Vera, Cucumber Extract, Retinyl Palmitate',
                'how_to_use': 'Gently pat a pea-sized amount around orbital bone morning and night. Never pull or rub. Keep refrigerated for extra de-puffing effect.',
                'skin_type': 'all',
                'original_price': 1199,
                'discount_price': 999,
                'stock': 40,
                'weight': '15ml',
                'is_featured': True,
                'tags': 'eye cream, dark circles, puffiness, caffeine',
            },
            # Face Masks
            {
                'name': 'Kaolin Clay Detox Mask',
                'slug': 'kaolin-clay-detox-mask',
                'category': 'face-masks',
                'brand': 'GLOW UP',
                'description': 'A deep-cleansing clay mask with kaolin and bentonite clay that draws out impurities, unclogs pores, and absorbs excess oil. Enriched with tea tree and charcoal for extra purification.',
                'ingredients': 'Kaolin Clay, Bentonite Clay, Activated Charcoal, Tea Tree Oil, Aloe Vera, Witch Hazel',
                'how_to_use': 'Apply thin layer to face avoiding eye area. Leave for 10-15 minutes until dry. Rinse thoroughly. Use once or twice a week.',
                'skin_type': 'oily',
                'original_price': 799,
                'discount_price': 649,
                'stock': 55,
                'weight': '75ml',
                'is_new_arrival': True,
                'tags': 'clay mask, detox, pores, oily skin',
            },
            # Toner
            {
                'name': 'Rose Water Balancing Toner',
                'slug': 'rose-water-balancing-toner',
                'category': 'toners',
                'brand': 'GLOW UP',
                'description': 'An alcohol-free hydrating toner with pure Bulgarian rose water that balances skin pH, tightens pores, and preps skin to better absorb serums and moisturizers.',
                'ingredients': 'Bulgarian Rose Water 70%, Glycerin, Niacinamide, Aloe Vera, Hyaluronic Acid, Centella Asiatica',
                'how_to_use': 'After cleansing, apply with a cotton pad or gently pat directly onto face. Use morning and evening.',
                'skin_type': 'all',
                'original_price': 599,
                'discount_price': None,
                'stock': 65,
                'weight': '200ml',
                'is_trending': True,
                'tags': 'rose water, toner, hydrating, pH balance',
            },
            # Lip Care
            {
                'name': 'Honey & Shea Lip Butter',
                'slug': 'honey-shea-lip-butter',
                'category': 'lip-care',
                'brand': 'GLOW UP',
                'description': 'An ultra-nourishing lip treatment with raw honey, shea butter, and vitamin E that heals chapped lips overnight. With a subtle golden tint that enhances natural lip colour.',
                'ingredients': 'Shea Butter, Raw Honey, Vitamin E, Jojoba Oil, Beeswax, Rosehip Oil, Sweet Almond Oil',
                'how_to_use': 'Apply liberally throughout the day and generously before bed. Can be used as an overnight lip mask.',
                'skin_type': 'all',
                'original_price': 449,
                'discount_price': 349,
                'stock': 90,
                'weight': '10g',
                'is_new_arrival': True,
                'tags': 'lip balm, honey, shea butter, chapped lips',
            },
        ]

        for p in products_data:
            cat_slug = p.pop('category')
            category = cats.get(cat_slug)
            if not category:
                continue
            obj, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={**p, 'category': category, 'is_available': True}
            )
            if created:
                self.stdout.write(f'  ✓ Product: {obj.name}')

        # ── Coupons ───────────────────────────────────────────────────────────
        coupons_data = [
            {
                'code': 'GLOW10',
                'discount_type': 'percent',
                'discount_value': 10,
                'min_order_amount': 500,
                'description': '10% off on orders above ₹500',
                'max_uses': 500,
            },
            {
                'code': 'WELCOME20',
                'discount_type': 'percent',
                'discount_value': 20,
                'min_order_amount': 999,
                'description': '20% welcome discount on orders above ₹999',
                'max_uses': 200,
            },
            {
                'code': 'SAVE100',
                'discount_type': 'fixed',
                'discount_value': 100,
                'min_order_amount': 799,
                'description': 'Flat ₹100 off on orders above ₹799',
                'max_uses': 300,
            },
            {
                'code': 'GLOW25',
                'discount_type': 'percent',
                'discount_value': 25,
                'min_order_amount': 1499,
                'description': '25% off on orders above ₹1499',
                'max_uses': 100,
            },
        ]

        now = timezone.now()
        for c in coupons_data:
            obj, created = Coupon.objects.get_or_create(
                code=c['code'],
                defaults={
                    **c,
                    'valid_from': now,
                    'valid_until': now + timedelta(days=365),
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Coupon: {obj.code}')

        # ── Offers ────────────────────────────────────────────────────────────
        offers_data = [
            {
                'title': 'Summer Hydration Sale',
                'description': 'Beat the heat with our best hydrating products',
                'discount_percent': 30,
                'url': '/products/?skin_type=dry',
            },
            {
                'title': 'New Arrivals Special',
                'description': 'Try our latest launches at exclusive prices',
                'discount_percent': 20,
                'url': '/products/?sort=newest',
            },
            {
                'title': 'Serum Bundle Deals',
                'description': 'Mix and match serums for your routine',
                'discount_percent': 15,
                'url': '/products/?category=serums',
            },
        ]

        for o in offers_data:
            obj, created = Offer.objects.get_or_create(
                title=o['title'],
                defaults={
                    **o,
                    'valid_until': date.today() + timedelta(days=90),
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Offer: {obj.title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data loaded successfully!'))
        self.stdout.write(self.style.WARNING('\nNext steps:'))
        self.stdout.write('  1. Add product images via Django Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('  2. Create a superuser: python manage.py createsuperuser')
        self.stdout.write('  3. Run server: python manage.py runserver')
