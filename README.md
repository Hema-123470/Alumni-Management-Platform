# Alumni Management System — Phase 1

Django + MySQL + Bootstrap alumni management system.

---

## Project Structure

```
alumni_management/       ← Django project config
    settings.py
    urls.py
accounts/                ← Auth & user management app
    models.py            ← CustomUser model (admin/alumni roles)
    views.py             ← login, register, dashboard, approvals
    forms.py             ← Registration & login forms
    urls.py
    admin.py
templates/
    base.html            ← Base layout with navbar + sidebar
    accounts/
        login.html
        register.html
        dashboard.html
        pending_approvals.html
static/                  ← CSS/JS assets (Bootstrap via CDN)
media/                   ← Uploaded files
manage.py
```

---

## Setup Instructions

### 1. Create MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE alumni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Update Database Password

Edit `alumni_management/settings.py` and update:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alumni_db',
        'USER': 'root',
        'PASSWORD': 'YOUR_ACTUAL_MYSQL_PASSWORD',  # ← change this
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Admin Superuser

```bash
python manage.py createsuperuser
```

When prompted, enter email, username, and password.
After creation, open the Django shell to set the role:

```bash
python manage.py shell
```

```python
from accounts.models import CustomUser
u = CustomUser.objects.get(email='your@email.com')
u.role = 'admin'
u.is_approved = True
u.save()
exit()
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## URLs

| URL                    | Description                        |
|------------------------|------------------------------------|
| `/login/`              | Login page                         |
| `/register/`           | Alumni self-registration           |
| `/dashboard/`          | Dashboard (admin or alumni view)   |
| `/pending-approvals/`  | Admin: review registrations        |
| `/approve/<id>/`       | Admin: approve an alumni           |
| `/reject/<id>/`        | Admin: reject an alumni            |
| `/admin/`              | Django admin panel                 |

---

## User Roles

| Role   | Capabilities                                              |
|--------|-----------------------------------------------------------|
| Admin  | Approve/reject alumni, view stats, manage all modules     |
| Alumni | View dashboard, profile (more features in Phase 2+)       |

Alumni accounts are **inactive until approved** by an admin.

---

## Phase Roadmap

- ✅ **Phase 1** — Project setup, auth, custom user model, Bootstrap UI
- 🔜 **Phase 2** — Alumni profiles, events, job postings
- 🔜 **Phase 3** — Donations, alumni directory, email notifications
- 🔜 **Phase 4** — Admin reports, UI polish, deployment prep
