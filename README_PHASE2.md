# Alumni Management System — Phase 2 Complete ✅

Django + MySQL + Bootstrap alumni management system with **profiles, events, and job postings**.

---

## What's New in Phase 2

### 1. Alumni Profile Module
- **Extended profiles** with academic, professional, and personal info
- Fields: batch year, department, degree, company, designation, industry, skills, location, bio, profile picture
- Alumni can **create and update** their own profiles
- Admin can **view all alumni** in a directory
- **Profile pages** with read-only view for other users

### 2. Event Management Module
- Admin can **create, edit, delete** events
- Event fields: title, description, type, venue, date/time, registration deadline, banner image
- Alumni can **view events** and **register** for them
- Event types: Seminar, Workshop, Reunion, Webinar, Networking, Other
- **Registration tracking** — see who registered for each event
- **Status badges**: Upcoming, Past, Open/Closed registration

### 3. Job Posting & Referral Module
- Admin can **post, edit, delete** job openings
- Job fields: title, company, location, type, description, requirements, salary range, apply link, deadline
- Job types: Full Time, Part Time, Internship, Contract, Remote
- Alumni can **view jobs** and **refer candidates** (name + email + note)
- Admin can **view all referrals** for each job
- **Apply links** redirect to external job portals

---

## Updated URLs

| URL                    | Description                        | Access       |
|------------------------|------------------------------------|--------------|
| `/login/`              | Login page                         | Public       |
| `/register/`           | Alumni self-registration           | Public       |
| `/dashboard/`          | Dashboard (admin or alumni view)   | Authenticated|
| `/profile/`            | My profile (edit)                  | Alumni       |
| `/profile/<id>/`       | View another alumni's profile      | Authenticated|
| `/alumni-list/`        | Alumni directory                   | Admin        |
| `/events/`             | Event list                         | Authenticated|
| `/events/<id>/`        | Event detail                       | Authenticated|
| `/events/create/`      | Create event                       | Admin        |
| `/events/<id>/edit/`   | Edit event                         | Admin        |
| `/events/<id>/delete/` | Delete event                       | Admin        |
| `/events/<id>/register/` | Register for event               | Alumni       |
| `/jobs/`               | Job list                           | Authenticated|
| `/jobs/<id>/`          | Job detail                         | Authenticated|
| `/jobs/create/`        | Post job                           | Admin        |
| `/jobs/<id>/edit/`     | Edit job                           | Admin        |
| `/jobs/<id>/delete/`   | Delete job                         | Admin        |
| `/jobs/<id>/refer/`    | Submit referral                    | Alumni       |
| `/jobs/<id>/referrals/`| View all referrals                 | Admin        |
| `/pending-approvals/`  | Review registrations               | Admin        |
| `/admin/`              | Django admin panel                 | Superuser    |

---

## Database Models

### Phase 1 Models
- **CustomUser** — email-based auth, roles (admin/alumni), approval system

### Phase 2 Models
- **AlumniProfile** — extended profile (1-to-1 with CustomUser)
- **Event** — event details, created by admin
- **EventRegistration** — tracks alumni event registrations
- **Job** — job postings, created by admin
- **JobReferral** — alumni refer candidates for jobs

---

## Setup Instructions

### 1. Create MySQL Database

```sql
CREATE DATABASE alumni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Update Database Password

Edit `alumni_management/settings.py`:

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

This will create all tables for Phase 1 + Phase 2.

### 4. Create Admin Superuser

```bash
python setup_admin.py
```

Or manually:

```bash
python manage.py createsuperuser
```

Then set role to admin:

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

## Features by Role

### Admin
- ✅ Approve/reject alumni registrations
- ✅ View all alumni in directory
- ✅ Create, edit, delete events
- ✅ Create, edit, delete job postings
- ✅ View all event registrations
- ✅ View all job referrals
- ✅ Dashboard with stats (alumni count, events, jobs, pending approvals)

### Alumni
- ✅ Create and update profile (academic, professional, personal info)
- ✅ Upload profile picture
- ✅ View other alumni profiles
- ✅ Browse and register for events
- ✅ Browse job postings
- ✅ Refer candidates for jobs
- ✅ Dashboard with profile summary

---

## Phase Roadmap

- ✅ **Phase 1** — Project setup, auth, custom user model, Bootstrap UI
- ✅ **Phase 2** — Alumni profiles, events, job postings
- 🔜 **Phase 3** — Donations, alumni directory with search/filter, email notifications
- 🔜 **Phase 4** — Admin reports, UI polish, deployment prep

---

## Tech Stack

- **Backend**: Django 6.0.3
- **Database**: MySQL (via mysqlclient 2.2.8)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Icons**: Bootstrap Icons
- **Python**: 3.14.3

---

## Next Steps

Run migrations and start the server:

```bash
python manage.py migrate
python setup_admin.py
python manage.py runserver
```

Then:
1. Log in as admin
2. Approve any pending alumni registrations
3. Create some events and job postings
4. Log in as an alumni user and test profile creation, event registration, and job referrals

Ready for **Phase 3** whenever you are! 🚀
