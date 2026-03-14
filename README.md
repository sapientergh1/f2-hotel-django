# F2 Hotel & Apartment — Django Website

A complete hotel booking website for **F2 Hotel & Apartment**, Kumasi, Ghana.
Built with Django 4.2, Bootstrap 5, and Paystack payment integration.

---

## 📁 Project Structure

```
hotel_project/
├── manage.py
├── requirements.txt
├── hotel_project/          # Main Django config
│   ├── settings.py
│   └── urls.py
├── accounts/               # User auth & profiles
├── rooms/                  # Room management & gallery
├── bookings/               # Booking system
├── payments/               # Paystack integration
├── website/                # Public pages (home, about, contact)
├── templates/              # All HTML templates
│   ├── base.html
│   ├── website/
│   ├── rooms/
│   ├── bookings/
│   ├── payments/
│   └── accounts/
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## ⚡ Quick Setup

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure settings
Edit `hotel_project/settings.py` and update:
- `SECRET_KEY` — change to a secure random string
- `PAYSTACK_SECRET_KEY` — your Paystack secret key
- `PAYSTACK_PUBLIC_KEY` — your Paystack public key
- Email settings (for booking confirmations)

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Seed sample room data
```bash
python manage.py seed_data
```

### 7. Collect static files (production)
```bash
python manage.py collectstatic
```

### 8. Run development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🔑 Paystack Setup

1. Sign up at https://paystack.com
2. Get your **Test** API keys from the dashboard
3. Set them in `settings.py`:
   ```python
   PAYSTACK_SECRET_KEY = 'sk_test_...'
   PAYSTACK_PUBLIC_KEY = 'pk_test_...'
   ```
4. Add your webhook URL in Paystack dashboard:
   `https://yourdomain.com/payments/webhook/`

---

## 🎨 Features

### Public Website
- **Home** — Hero banner, booking search, featured rooms, amenities, gallery, testimonials
- **About** — Hotel story, values, room types, location map
- **Rooms** — Filterable room listing with search by dates/guests/type
- **Room Detail** — Full room info, gallery, amenities, sticky booking sidebar
- **Gallery** — Filterable photo gallery
- **Contact** — Contact form, map, info

### Booking System
- Search available rooms by date, guests, type
- Prevents double-booking via conflict detection
- Price preview before confirming
- Booking reference number generated automatically

### Payments (Paystack)
- Paystack inline payment popup
- Payment verification via Paystack API
- Webhook for server-side confirmation
- Booking status auto-updates on successful payment

### User Dashboard
- Register / Login / Logout
- View active and past bookings
- Cancel eligible bookings
- Update profile information

### Admin Panel (`/admin/`)
- Manage rooms (add, edit, upload images, set prices)
- Manage bookings (view, change status)
- Manage users and payments
- Gallery management

---

## 🏨 Room Types

| Type       | Starting Price | Capacity |
|------------|---------------|----------|
| Standard   | GHS 250/night | 2 guests |
| Deluxe     | GHS 380/night | 2 guests |
| Executive  | GHS 500/night | 2 guests |
| Family     | GHS 550/night | 5 guests |
| Apartment  | GHS 600/night | 2 guests |

---

## 📦 Tech Stack

- **Backend**: Python 3.10+, Django 4.2
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Bootstrap 5.3, Font Awesome 6, Google Fonts
- **Payments**: Paystack
- **Media**: Django file uploads with Pillow
- **Fonts**: Playfair Display + Jost

---

## 🌍 Hotel Location

**F2 Hotel & Apartment**
Akom, Custom Check Point, Off Offinso Road,
Kumasi, Ashanti Region, Ghana
