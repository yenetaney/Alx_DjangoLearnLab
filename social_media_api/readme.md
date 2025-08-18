# Django REST API – User Authentication & Profile

This project is a modular Django REST API that handles user registration, login, and profile access using token-based authentication and a custom user model.

## 🔧 Features

- User registration with token creation
- Secure login with token return
- Custom user model (`AbstractUser`)
- Token-based authentication (`TokenAuthentication`)
- Protected profile endpoint (`/profile`)
- Password hashing and validation
- Modular structure with serializers, views, and models

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yenetaney/Alx_DjangoLearnLab.git
cd social_media_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
