# Capstone Project: HR Services & Resume Management Platform

## Overview

This project is a full-stack web application built with **Django** and **JavaScript** that provides a centralized platform for managing resumes and HR-related services. The application allows users to upload, store, view, and manage resumes, while HR administrators can organize candidate information, track submissions, and interact with stored data dynamically through a modern, responsive interface.

The goal of this project was to design and implement a non-trivial, original web application that goes beyond the scope of previous CS50W projects by combining structured data models, dynamic JavaScript-based interactions, and a real-world use case commonly found in professional HR systems.

---

## Distinctiveness and Complexity

### Distinctiveness

This project is **distinct from all other projects in the CS50W course**:

- It is **not a social network**: there are no user posts, follows, likes, or feeds.
- It is **not an e-commerce platform**: no shopping carts, payments, or product purchasing workflows.
- It is **not based on the CS50 Pizza project** or any earlier course example.

Instead, this application focuses on **HR workflow management**, specifically resume handling and candidate organization, which was not explored in any prior assignment. The domain (HR services and resume tracking) introduces a different problem space centered around document management, structured candidate data, and administrative tools.

### Complexity

The project demonstrates significant complexity through:

- **Multiple Django models** representing resumes and HR-related entities
- **File uploads and storage** using Django’s media handling
- **Dynamic JavaScript functionality** for loading, filtering, and managing data without full page reloads
- **REST-style endpoints** returning JSON responses
- **Mobile-responsive design** using CSS and layout best practices
- **Separation of concerns** between backend logic, frontend templates, and static JavaScript files

Compared to previous projects, this application required deeper planning around data relationships, validation, and UI/UX flow, making it substantially more complex.

---

## File Structure and Contents

### Root Directory
- `manage.py` – Django’s command-line utility for administrative tasks
- `db.sqlite3` – SQLite database used during development
- `.gitignore` – Specifies files and folders ignored by Git
- `requirements.txt` – Lists Python dependencies required to run the project
- `README.md` – Documentation and project explanation

### capstone/
- `__init__.py` – Marks the directory as a Python package
- `settings.py` – Main Django settings file
- `urls.py` – URL routing for the entire project
- `asgi.py` – ASGI configuration for asynchronous deployment
- `wsgi.py` – WSGI configuration for production servers

### HRservices/
- `models.py` – Defines database models related to HR services
- `views.py` – Handles backend logic and API responses
- `urls.py` – App-specific URL routing
- `templates/` – HTML templates rendered by Django
- `static/` – JavaScript and CSS files used for dynamic behavior and styling

### resumes/
- Handles resume-specific functionality, including upload, storage, and display
- Contains models, views, and templates related to resume management

---

## How to Run the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/me50/USERNAME.git
   cd capstone

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

https://127.0.0.1:8000/
