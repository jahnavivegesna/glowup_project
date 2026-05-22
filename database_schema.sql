-- ============================================================
-- GLOW UP — MySQL Database Schema
-- Run Django migrations instead of this file directly.
-- This is for reference / manual setup only.
-- ============================================================

CREATE DATABASE IF NOT EXISTS glowup_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE glowup_db;

-- ─── Categories ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_category (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  slug        VARCHAR(100) NOT NULL UNIQUE,
  image       VARCHAR(255),
  description TEXT,
  is_active   TINYINT(1) DEFAULT 1,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─── Products ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_product (
  id               BIGINT AUTO_INCREMENT PRIMARY KEY,
  category_id      BIGINT NOT NULL,
  name             VARCHAR(200) NOT NULL,
  slug             VARCHAR(200) NOT NULL UNIQUE,
  brand            VARCHAR(100) DEFAULT 'GLOW UP',
  description      LONGTEXT NOT NULL,
  ingredients      LONGTEXT,
  how_to_use       LONGTEXT,
  skin_type        VARCHAR(20) DEFAULT 'all',
  original_price   DECIMAL(10,2) NOT NULL,
  discount_price   DECIMAL(10,2),
  discount_percent INT DEFAULT 0,
  image            VARCHAR(255) NOT NULL,
  image2           VARCHAR(255),
  image3           VARCHAR(255),
  stock            INT DEFAULT 0,
  is_available     TINYINT(1) DEFAULT 1,
  is_featured      TINYINT(1) DEFAULT 0,
  is_new_arrival   TINYINT(1) DEFAULT 0,
  is_trending      TINYINT(1) DEFAULT 0,
  weight           VARCHAR(50),
  tags             VARCHAR(200),
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES store_category(id) ON DELETE CASCADE
);

-- ─── User Profiles ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_userprofile (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id       INT NOT NULL UNIQUE,
  phone         VARCHAR(15),
  avatar        VARCHAR(255),
  date_of_birth DATE,
  skin_type     VARCHAR(20),
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city          VARCHAR(100),
  state         VARCHAR(100),
  pincode       VARCHAR(10),
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- ─── Reviews ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_review (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  product_id  BIGINT NOT NULL,
  user_id     INT NOT NULL,
  rating      INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  title       VARCHAR(200),
  body        LONGTEXT NOT NULL,
  is_verified TINYINT(1) DEFAULT 0,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_review (product_id, user_id),
  FOREIGN KEY (product_id) REFERENCES store_product(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- ─── Cart ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_cart (
  id         BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id    INT NOT NULL UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS store_cartitem (
  id         BIGINT AUTO_INCREMENT PRIMARY KEY,
  cart_id    BIGINT NOT NULL,
  product_id BIGINT NOT NULL,
  quantity   INT DEFAULT 1,
  added_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cart_id) REFERENCES store_cart(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES store_product(id) ON DELETE CASCADE
);

-- ─── Wishlist ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_wishlist (
  id         BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id    INT NOT NULL UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS store_wishlist_products (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  wishlist_id BIGINT NOT NULL,
  product_id  BIGINT NOT NULL,
  UNIQUE KEY unique_wishlist_product (wishlist_id, product_id),
  FOREIGN KEY (wishlist_id) REFERENCES store_wishlist(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES store_product(id) ON DELETE CASCADE
);

-- ─── Coupons ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_coupon (
  id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
  code               VARCHAR(50) NOT NULL UNIQUE,
  discount_type      VARCHAR(10) DEFAULT 'percent',
  discount_value     DECIMAL(10,2) NOT NULL,
  min_order_amount   DECIMAL(10,2) DEFAULT 0,
  max_uses           INT DEFAULT 100,
  used_count         INT DEFAULT 0,
  valid_from         DATETIME NOT NULL,
  valid_until        DATETIME NOT NULL,
  is_active          TINYINT(1) DEFAULT 1,
  description        VARCHAR(200)
);

-- ─── Orders ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_order (
  id              BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id        VARCHAR(20) NOT NULL UNIQUE,
  user_id         INT NOT NULL,
  coupon_id       BIGINT,
  status          VARCHAR(20) DEFAULT 'pending',
  payment_method  VARCHAR(20) DEFAULT 'cod',
  full_name       VARCHAR(200) NOT NULL,
  phone           VARCHAR(15) NOT NULL,
  email           VARCHAR(254) NOT NULL,
  address_line1   VARCHAR(255) NOT NULL,
  address_line2   VARCHAR(255),
  city            VARCHAR(100) NOT NULL,
  state           VARCHAR(100) NOT NULL,
  pincode         VARCHAR(10) NOT NULL,
  subtotal        DECIMAL(10,2) NOT NULL,
  discount_amount DECIMAL(10,2) DEFAULT 0,
  shipping_charge DECIMAL(10,2) DEFAULT 0,
  total           DECIMAL(10,2) NOT NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  delivered_at    DATETIME,
  FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
  FOREIGN KEY (coupon_id) REFERENCES store_coupon(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS store_orderitem (
  id             BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id       BIGINT NOT NULL,
  product_id     BIGINT NOT NULL,
  product_name   VARCHAR(200) NOT NULL,
  product_price  DECIMAL(10,2) NOT NULL,
  quantity       INT NOT NULL,
  total_price    DECIMAL(10,2) NOT NULL,
  image_url      VARCHAR(500),
  FOREIGN KEY (order_id) REFERENCES store_order(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES store_product(id) ON DELETE CASCADE
);

-- ─── Newsletter ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_newslettersubscription (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(254) NOT NULL UNIQUE,
  name          VARCHAR(100),
  subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_active     TINYINT(1) DEFAULT 1
);

-- ─── Offers ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_offer (
  id               BIGINT AUTO_INCREMENT PRIMARY KEY,
  title            VARCHAR(200) NOT NULL,
  description      LONGTEXT NOT NULL,
  image            VARCHAR(255),
  discount_percent INT DEFAULT 0,
  valid_until      DATE NOT NULL,
  is_active        TINYINT(1) DEFAULT 1,
  url              VARCHAR(200),
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─── Sample Insert: Coupons ────────────────────────────────────
INSERT IGNORE INTO store_coupon (code, discount_type, discount_value, min_order_amount, max_uses, valid_from, valid_until, is_active, description) VALUES
('GLOW10',    'percent', 10,  500,  500, NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR), 1, '10% off on orders above Rs 500'),
('WELCOME20', 'percent', 20,  999,  200, NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR), 1, '20% welcome discount'),
('SAVE100',   'fixed',   100, 799,  300, NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR), 1, 'Flat Rs 100 off'),
('GLOW25',    'percent', 25,  1499, 100, NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR), 1, '25% off on orders above Rs 1499');
