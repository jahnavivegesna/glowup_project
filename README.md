# 🌿 GLOW UP — Luxury Skincare E-Commerce

> **Full-stack Django + MySQL skincare store with pastel gold/green theme, dark mode, cart, wishlist, orders, dashboard, and admin panel.**

---

## 📁 Project Structure

```
glowup/
├── glowup_project/          # Django project config
│   ├── settings.py          # All settings (DB, static, email, etc.)
│   ├── urls.py              # Root URL routing
│   └── wsgi.py
│
├── store/                   # Main Django app
│   ├── models.py            # Database models (Product, Order, Cart, etc.)
│   ├── views.py             # All views/page logic
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # All Django forms
│   ├── admin.py             # Admin panel configuration
│   ├── signals.py           # Auto-create Profile/Cart/Wishlist on signup
│   ├── context_processors.py
│   └── management/
│       └── commands/
│           └── load_sample_data.py   # Demo data loader
│
├── templates/               # All HTML templates
│   ├── base.html            # Master layout (navbar, footer, dark mode)
│   └── store/
│       ├── home.html        # Hero, featured, new arrivals, reviews
│       ├── products.html    # Grid + filters + pagination
│       ├── product_detail.html  # Gallery, zoom, reviews, related
│       ├── cart.html        # Cart with AJAX quantity update
│       ├── checkout.html    # Shipping form + coupon
│       ├── order_success.html
│       ├── dashboard.html   # User dashboard
│       ├── order_history.html
│       ├── order_detail.html
│       ├── profile.html
│       ├── wishlist.html
│       ├── coupons.html
│       ├── search.html
│       ├── about.html
│       ├── contact.html
│       ├── register.html
│       ├── login.html
│       └── partials/
│           └── product_card.html    # Reusable product card
│
├── static/
│   ├── css/style.css        # Complete CSS (variables, dark mode, responsive)
│   └── js/main.js           # All JS (cart AJAX, wishlist, dark mode, animations)
│
├── media/                   # User-uploaded images (auto-created)
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Setup Instructions

### Step 1 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — MySQL Database Setup

Open MySQL shell or MySQL Workbench and run:

```sql
CREATE DATABASE glowup_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'glowup_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON glowup_db.* TO 'glowup_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 4 — Configure Database in settings.py

Edit `glowup_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'glowup_db',
        'USER': 'glowup_user',      # Your MySQL username
        'PASSWORD': 'yourpassword',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Enter username, email, and password when prompted
```

### Step 7 — Load Sample Data

```bash
python manage.py load_sample_data
```

This creates:
- 8 product categories
- 12 skincare products with descriptions
- 4 discount coupons (GLOW10, WELCOME20, SAVE100, GLOW25)
- 3 promotional offers

### Step 8 — Collect Static Files

```bash
python manage.py collectstatic
```

### Step 9 — Run the Development Server

```bash
python manage.py runserver
```

Open in browser:
- 🌐 **Website:** http://127.0.0.1:8000/
- 🔧 **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🎨 Features Overview

### Frontend
| Feature | Status |
|---------|--------|
| Responsive design (mobile/tablet/desktop) | ✅ |
| Dark mode toggle (persisted in localStorage) | ✅ |
| Smooth scroll animations (IntersectionObserver) | ✅ |
| Product card hover effects + image zoom | ✅ |
| Sticky navbar with scroll effect | ✅ |
| Search overlay (press `/` to open) | ✅ |
| Toast notifications | ✅ |
| Auto-scrolling trending carousel | ✅ |
| Glassmorphism & soft card design | ✅ |

### Backend / Functionality
| Feature | Status |
|---------|--------|
| User registration & login (email or username) | ✅ |
| Password encryption (Django built-in) | ✅ |
| Auto-create Profile + Cart + Wishlist on signup | ✅ |
| Product catalog with categories & filters | ✅ |
| Skin type, price range, sort filters | ✅ |
| Add/remove/update cart (AJAX) | ✅ |
| Wishlist toggle (AJAX) | ✅ |
| Coupon code system (% or fixed) | ✅ |
| Cash on Delivery checkout | ✅ |
| Order confirmation with order ID | ✅ |
| User dashboard with order history | ✅ |
| Admin panel with full CRUD | ✅ |
| Newsletter subscription | ✅ |
| Product reviews & ratings | ✅ |
| Related products | ✅ |

---

## 🔑 Admin Panel Features

Visit `/admin/` with your superuser credentials.

| Section | What You Can Do |
|---------|----------------|
| **Products** | Add/Edit/Delete products, upload images, set featured/new/trending flags |
| **Categories** | Manage product categories |
| **Orders** | View all orders, update order status (Pending → Shipped → Delivered) |
| **Users** | Manage registered users |
| **Coupons** | Create/disable discount codes |
| **Newsletter** | View all subscribers |
| **Offers** | Create promotional banners |
| **Reviews** | Moderate customer reviews |

---

## 🏷️ Available Coupon Codes (Sample)

| Code | Discount | Minimum Order |
|------|----------|---------------|
| `GLOW10` | 10% off | ₹500 |
| `WELCOME20` | 20% off | ₹999 |
| `SAVE100` | ₹100 off | ₹799 |
| `GLOW25` | 25% off | ₹1499 |

---

## 🖼️ Adding Product Images

1. Log in to Admin Panel: http://127.0.0.1:8000/admin/
2. Go to **Store → Products**
3. Click any product → scroll to **Images** section
4. Upload product images (supports main image + 2 additional views)
5. Save

**Recommended image size:** 800×800px square, JPG/PNG/WebP

---

## 📧 Email Configuration

Currently set to console backend (emails print in terminal). For production:

```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password
```

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Django 4.2 |
| Database | MySQL 8.0 |
| Frontend | HTML5, CSS3 (custom), Vanilla JS |
| Fonts | Cormorant Garamond, DM Sans, Satisfy |
| Icons | Font Awesome 6 |
| Auth | Django built-in auth |
| Images | Pillow |
| Static | WhiteNoise |

---

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing (PBKDF2 + SHA256)
- Session-based authentication
- SQL injection protection (Django ORM)
- XSS protection (Django template escaping)
- Login required decorators on all protected views
- User can only view their own orders/profile

---

## 📱 Responsive Breakpoints

| Breakpoint | Layout |
|-----------|--------|
| Desktop (1200px+) | 4-column product grid, sidebar filters, split layouts |
| Tablet (768–1024px) | 2-column grid, collapsed sidebar |
| Mobile (< 768px) | 1-2 column grid, hamburger menu, full-width forms |

---

## 🌙 Color Palette

| Variable | Value | Usage |
|----------|-------|-------|
| `--gold` | `#C9A96E` | Primary accents, CTAs, prices |
| `--green` | `#7BAD7E` | Secondary accents, success states |
| `--cream` | `#FAF7F2` | Main background |
| `--text-primary` | `#2C2416` | Headings, body text |
| `--gold-dark` | `#A07840` | Hover states |
| `--green-dark` | `#4E7D52` | Dark green accents |

---

## 📝 Notes for College Submission

This project demonstrates:
1. **MVC Architecture** — Models (store/models.py), Views (store/views.py), Templates (templates/)
2. **Database Design** — Normalized MySQL schema with proper FK relationships
3. **User Authentication** — Registration, login, logout, session management
4. **AJAX/Dynamic UI** — Cart updates, wishlist toggling, coupon application without page reload
5. **Responsive Design** — CSS Grid, Flexbox, media queries for all screen sizes
6. **Security** — CSRF, password hashing, login_required decorators
7. **Clean Code** — Comments, consistent naming, modular templates, reusable components

---

*Built with 💛 | GLOW UP Luxury Skincare*
