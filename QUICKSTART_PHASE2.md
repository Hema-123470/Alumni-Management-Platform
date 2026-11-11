# 🚀 Quick Start — Phase 2

Get your Alumni Management System running in 3 minutes.

---

## Prerequisites

✅ Python 3.14.3  
✅ Django 6.0.3  
✅ mysqlclient 2.2.8  
✅ MySQL server running

---

## Step 1: Database Setup

Open MySQL and run:

```sql
CREATE DATABASE alumni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## Step 2: Configure Database Password

Edit `alumni_management/settings.py` line 65:

```python
'PASSWORD': 'your_actual_mysql_password',  # ← Change this
```

---

## Step 3: Run Migrations

```bash
python manage.py migrate
```

This creates all tables for:
- ✅ User authentication (Phase 1)
- ✅ Alumni profiles (Phase 2)
- ✅ Events (Phase 2)
- ✅ Jobs (Phase 2)

---

## Step 4: Create Admin User

```bash
python setup_admin.py
```

Enter:
- Email
- Username
- First Name
- Last Name
- Password

The script automatically sets:
- `role = 'admin'`
- `is_approved = True`
- `is_staff = True`
- `is_superuser = True`

---

## Step 5: Start Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🎯 Test the System

### As Admin:
1. Log in with your admin credentials
2. **Dashboard** → See stats (0 alumni, 0 events, 0 jobs initially)
3. **Approvals** → No pending approvals yet
4. **Events** → Click "Create Event" → Fill form → Save
5. **Jobs** → Click "Post Job" → Fill form → Save
6. **Alumni List** → Empty (no alumni registered yet)

### Register an Alumni:
1. Log out
2. Click "Register here"
3. Fill registration form
4. Submit → "Registration successful! Pending admin approval."

### Approve Alumni:
1. Log back in as admin
2. **Dashboard** → See "1 Pending Approval"
3. Click "View All" or go to **Approvals**
4. Click "Approve" on the pending user

### Test as Alumni:
1. Log out
2. Log in with the approved alumni credentials
3. **My Profile** → Fill out profile (batch, company, skills, etc.) → Save
4. **Events** → Click on an event → "Register Now"
5. **Jobs** → Click on a job → Fill referral form → Submit

### Back to Admin:
1. Log in as admin
2. **Events** → Click event → See "1 registered"
3. **Jobs** → Click job → "Referrals" button → See submitted referral

---

## 📂 What You Have Now

### Phase 1 ✅
- Custom user model with roles (admin/alumni)
- Email-based authentication
- Alumni registration with admin approval
- Login/logout system
- Bootstrap UI with sidebar navigation

### Phase 2 ✅
- **Alumni Profiles** — Academic, professional, personal info + profile picture
- **Event Management** — Create events, alumni register, track registrations
- **Job Postings** — Post jobs, alumni refer candidates, track referrals
- **Alumni Directory** — Admin views all alumni profiles
- **Dashboard Stats** — Live counts for alumni, events, jobs, pending approvals

---

## 🔥 Key Features

| Feature | Admin | Alumni |
|---------|-------|--------|
| Approve registrations | ✅ | ❌ |
| View all alumni | ✅ | ❌ |
| Create/edit/delete events | ✅ | ❌ |
| Create/edit/delete jobs | ✅ | ❌ |
| View event registrations | ✅ | ❌ |
| View job referrals | ✅ | ❌ |
| Edit own profile | ✅ | ✅ |
| View other profiles | ✅ | ✅ |
| Register for events | ❌ | ✅ |
| Refer jobs | ❌ | ✅ |

---

## 🐛 Troubleshooting

### "Access denied for user 'root'@'localhost'"
→ Update MySQL password in `settings.py`

### "No module named 'mysqlclient'"
→ Run: `pip install mysqlclient`

### "Table doesn't exist"
→ Run: `python manage.py migrate`

### "CSRF verification failed"
→ Clear browser cookies and try again

### Images not showing
→ Make sure `media/` folder exists and check `MEDIA_URL` in settings

---

## 📚 Documentation

- **README_PHASE2.md** — Full feature list and setup guide
- **PHASE2_SUMMARY.md** — Technical implementation details
- **outline.txt** — Original 4-phase project plan

---

## ✨ Next: Phase 3

Phase 3 will add:
1. Donation & Sponsorship tracking
2. Alumni directory with search/filter (by skills, company, location, batch)
3. Email notifications for events and jobs

Ready when you are! 🚀
