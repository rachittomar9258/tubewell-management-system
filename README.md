# 🚜 Tubewell Management System

A full-stack Django web application built to digitize tubewell rental management for Indian villages — helping farmers and tubewell owners track usage, payments, and access in one place.

**🔗 Live Demo:** [https://tubewell-management-system.onrender.com](https://tubewell-management-system.onrender.com)

---

## 📌 About the Project

In many rural areas, tubewell owners rent out irrigation access to farmers, but usage and payment tracking is still done manually — often on paper. This project brings that process online with role-based dashboards, automated balance calculations, and a clean, mobile-friendly interface designed for real village use cases.

## ✨ Features

- **Role-based access control** — separate dashboards for Owners and Renters
- **Authorized renter management** — owners can link/unlink renters to specific tubewells
- **Usage tracking** — records tubewell usage per renter
- **Payment tracking** — automatic balance calculation between owners and renters
- **Secure authentication** — custom login/signup flow with Django's auth system
- **Admin panel** — full data management via Django Admin
- **Responsive UI** — works across mobile and desktop

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 (Python) |
| Database | PostgreSQL (hosted on Neon) |
| Static Files | WhiteNoise |
| Deployment | Render |
| Frontend | Django Templates, Bootstrap |

## 🚀 Deployment

This project is deployed on **Render** using:
- `gunicorn` as the WSGI server
- **Neon.tech** for managed PostgreSQL
- Environment-based configuration (`python-decouple`) for secrets
- Automatic migrations on deploy

## 📂 Project Structure

```
tubewell_system/
├── accounts/       # Custom user model, auth, signup/login
├── tubewells/      # Tubewell & authorized renter models
├── usage/          # Usage record tracking
├── payments/       # Payment & balance calculation logic
├── static/         # CSS, JS, images
├── templates/      # HTML templates
└── tubewell_system/  # Project settings & URLs
```

## 👤 Author

**Rachit**
BCA Graduate | Python & Django Developer
[LinkedIn](www.linkedin.com/in/rachittomar10) · [GitHub](https://github.com/rachittomar9258)

---

*Note: Hosted on Render's free tier — the app may take 30–50 seconds to load on first request after inactivity (cold start).*
