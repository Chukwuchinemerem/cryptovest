# 🚀 CryptoVest – AI-Powered Crypto Investment Platform

A complete, production-ready Django investment platform with:
- Premium hero carousel (5 slides, autoplay)
- Language selector (20+ languages)
- Live withdrawal popup notifications
- Full user dashboard with referral program
- Admin panel at `/admin_dashboard/`
- Automatic daily profit calculation
- 5 investment plans (Starter → Diamond)

---

## ⚡ Quick Start (Local)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment (optional for dev)
cp .env.example .env
# Edit .env with your values (SECRET_KEY at minimum)

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (or use the command below)
python manage.py create_superuser
# Creates: username=Admin2, password=12345678

# 6. Start development server
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## 🔑 Access Points

| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/accounts/register/` | User registration |
| `/accounts/login/` | User login |
| `/dashboard/` | User dashboard |
| `/admin_dashboard/` | Custom admin panel |
| `/django-admin/` | Django built-in admin |

**Default Superuser:**
- Username: `Admin2`
- Password: `12345678`

⚠️ **Change the password immediately after first login!**

---

## 🌐 Deploy on Render

### 1. Push to GitHub
```bash
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/yourname/cryptovest.git
git push -u origin main
```

### 2. Create a Render Web Service
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Set these values:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn cryptovest.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Set Environment Variables in Render
| Key | Value |
|-----|-------|
| `SECRET_KEY` | (generate a 50-char random string) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `DATABASE_URL` | (from Render PostgreSQL addon) |

### 4. Add PostgreSQL Database
- Render Dashboard → New → PostgreSQL
- Copy the **Internal Database URL** → paste as `DATABASE_URL` env var

### 5. Deploy
Click **Deploy** — Render will run `build.sh` which:
1. Installs requirements
2. Runs migrations
3. Creates the superuser (`Admin2` / `12345678`)
4. Collects static files

---

## 💰 Investment Plans (Default)

| Plan | Min | Max | Daily % | Days | Total ROI |
|------|-----|-----|---------|------|-----------|
| Starter | $50 | $999 | 1.5% | 7 | 10.5% |
| Silver | $1,000 | $4,999 | 2.5% | 14 | 35% |
| Gold | $5,000 | $19,999 | 3.5% | 21 | 73.5% |
| Platinum | $20,000 | $49,999 | 5.0% | 30 | 150% |
| Diamond | $50,000 | $500,000 | 7.5% | 30 | 225% |

---

## 🛠 Admin Guide

### Process Daily Profits Manually
```bash
python manage.py process_profits
```

### Create Superuser
```bash
python manage.py create_superuser
```

### Set Up Cron Job (Render)
In Render, add a **Cron Job** service:
- Command: `python manage.py process_profits`
- Schedule: `0 0 * * *` (midnight daily)

---

## 📁 Project Structure
```
cryptovest_project/
├── cryptovest/          # Django settings, urls, wsgi
├── core/                # Landing page, investment plans, notifications
├── accounts/            # Auth: register, login, logout, user profiles
├── dashboard/           # User dashboard: invest, deposit, withdraw, referral
├── adminpanel/          # Custom admin panel at /admin_dashboard/
├── templates/           # All HTML templates
├── static/              # CSS, JS, images
├── requirements.txt
├── Procfile
├── build.sh
└── manage.py
```

---

## 📱 Customization

### Change WhatsApp Number
Search for `2349121304245` and replace with your number.

### Change Wallet Addresses
In `dashboard/views.py`, update the `CRYPTO_ADDRESSES` dict.

### Change Admin Credentials
Edit `core/management/commands/create_superuser.py`

---

## ⚠️ Important Notes
- Change `SECRET_KEY` before production deployment
- Update wallet addresses in `dashboard/views.py`
- Update WhatsApp number across templates
- Set `DEBUG=False` in production
- Use PostgreSQL (not SQLite) in production
