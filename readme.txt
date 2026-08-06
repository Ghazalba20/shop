# 🛒 Django Shop API

A RESTful online shop backend developed with Django and Django REST Framework.

## Features

### Authentication
- Register with phone number
- Verify phone number using OTP
- Resend verification code
- JWT Authentication (Access & Refresh Token)

### User
- Update profile
- Manage addresses
- View profile information

### Products
- Product List
- Product Detail
- Create Product (Admin)
- Update Product (Admin)
- Delete Product (Admin)
- Search Products
- Filter Products

### Basket
- Add to Basket
- Remove from Basket

### Favorites
- Add to Favorites
- Remove from Favorites

### Comments
- Create Comment
- Update Comment
- Delete Comment

### Orders
- Order List
- Order Detail
- Checkout

### Admin
- Manage Products
- Manage Product Features
- Manage Special Offers

### Fake Data
- Management command for generating fake data.

---

# Technologies

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Pillow

---

# Installation

Clone the repository

```bash
git clone https://github.com/Ghazalba20/shop.git
```

Go to project directory

```bash
cd shop
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

---

# Generate Fake Data

```bash
python manage.py seed_data
```

---

# User Roles

## Customer

- Register
- Login
- Verify phone
- Add products to basket
- Add products to favorites
- Place orders
- Write comments
- Manage profile
- Manage addresses

## Admin

- Add products
- Update products
- Delete products
- Manage product features
- Manage offers

---

# Authentication

JWT Authentication is used.

After login, include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

# Project Structure

```
shop/
│
├── account/
├── product/
├── order/
├── comment/
├── favorite/
├── basket/
├── profile/
├── config/
├── manage.py
└── requirements.txt
```

---

# API Highlights

- Authentication
- Products CRUD
- Product Search & Filter
- Basket APIs
- Favorites APIs
- Orders APIs
- Comments APIs
- Profile APIs
- Address APIs

---

# Developed By

**Ghazal Bakhtiary**

