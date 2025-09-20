# CoffeeShop

CoffeeShop is a Django project for managing a coffee shop system. It supports both a **web frontend** with templates and a **RESTful API** (nested inside `api/v1` folders for each app). The project also includes **Swagger documentation** for easy API exploration.

---

## 🚀 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation & Swagger](#api-documentation--swagger)
- [Email & Media](#email--media)
- [Database Schema](#database-schema)
- [Team & Roles](#team--roles)
- [Contributing](#contributing)
- [License](#license)

---

## About

CoffeeShop provides an online system for managing products, orders, and users. The repository includes:
- Full web app with Django templates for user interaction.
- Nested API code (`api/v1`) for programmatic access.
- Swagger documentation at `/swagger/` or `/api/docs/`.

---

## Features

- Full Django web app with templates
- RESTful API inside `api/v1` for each app
- JWT authentication (Simple JWT)
- Product, Order, and User management
- Pagination, filtering, and search for API endpoints
- Swagger documentation for interactive API exploration
- Email integration for notifications (Gmail SMTP)
- AWS S3 support for media files

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Frontend | Django Templates, HTML, CSS |
| Authentication | JWT (Simple JWT) + optional Session Auth |
| API Docs | Swagger (drf_yasg), DRF Spectacular |
| Storage | Local + AWS S3 (boto3, django-storages) |
| Database | SQLite (default) |
| Testing | Postman collection included |

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git
- Virtual environment tool (venv, virtualenv)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/firooz-hosseini/CoffeeShop.git
cd CoffeeShop
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables (.env) with:
```text
my_email=your_email@gmail.com
my_email_password=your_email_password
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_ENDPOINT_URL=...
AWS_S3_REGION_NAME=...
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Run the development server:
```bash
python manage.py runserver
```

Access the web frontend at `http://127.0.0.1:8000/`

---

## API Documentation & Swagger

- All API endpoints are nested under `/api/v1/` for each app.
- Postman collection (`CoffeeShop-API-postman`) included for testing.
- Swagger docs available at `/swagger/` or `/api/docs/`.

Example endpoint paths:
- `GET /api/v1/products/`
- `POST /api/v1/orders/`
- `GET /api/v1/accounts/profile/`

---

## Email & Media

- Email is configured using Gmail SMTP for notifications.
- Media files can be stored locally (`MEDIA_ROOT`) or on AWS S3.
- Static files are served from `STATICFILES_DIRS`.

---

## Database Schema

ERD diagrams included (`ERD.pdf`, `CoffeeShop ERD.drawio.pdf`) showing tables, relationships, and connections.

---

## Team & Roles

This project was developed by a team of three members as part of **Maktab130**.

| Role | Contributor |
|------|-------------|
| **Team Lead & Developer** | [Firooz Hosseini](https://github.com/firooz-hosseini) |
| Backend Developer | [Sina Rezaie](https://github.com/Sina-vd) |
| Backend Developer | [Erfaneh Eghbali](https://github.com/erfaneh-eghbali) |


**Responsibilities as Team Lead & Developer:**
- Designed the database schema (ERD)
- Developed the **accounts app**, including all views and logic
- Reviewed and improved team members’ code
- Managed media file storage on Arvan Cloud using **boto3** and **django-storages**
- Prepared the Postman collection for API testing
- Configured JWT authentication and Swagger documentation
- Managed Git workflow, code reviews, and task coordination
- Ensured deadlines and project milestones were met

---

## Contributing

We welcome contributions! To contribute:
1. **Fork** the repository
2. **Create a feature branch** for your changes (`git checkout -b feature/your-feature`)
3. **Commit your changes** with clear messages (`git commit -m "Add feature"`)
4. **Push** your branch to your fork (`git push origin feature/your-feature`)
5. **Open a Pull Request** for review
6. **Participate in the review process** and make requested changes
7. **Merge** will be done after approval

---

## License

For educational/group use.

