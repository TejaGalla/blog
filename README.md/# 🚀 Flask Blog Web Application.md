# 🚀 Flask Blog Web Application

A modern Flask blog web application with user authentication and full CRUD operations using MySQL and Bootstrap.

---

## 📌 Overview

This project is a full-stack blog application built using Python Flask, MySQL, HTML, and Bootstrap.  
It allows users to register, log in, add blog posts, view all posts, update existing posts, and delete posts through a clean web interface.

---

## 🎯 Features

- User Registration
- User Login and Logout
- Admin Dashboard
- Add New Blog Posts
- View All Posts
- Update Existing Posts
- Delete Posts
- MySQL Database Integration
- Responsive Bootstrap UI

---

## 🛠️ Tech Stack

- Backend: Python, Flask  
- Frontend: HTML, Bootstrap  
- Database: MySQL  
- Tools: VS Code, Git, GitHub  

---

## 📂 Project Structure

blog/
│── app.py
└── templates/
    │── navbar.html
    │── homepage.html
    │── login.html
    │── register.html
    │── admin.html
    │── add_post.html
    │── viewpost.html
    │── updatepost.html

---

## ⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/TejaGalla/blog.git  
cd blog  

2. Install packages

pip install flask mysql-connector-python werkzeug  

3. Create database

CREATE DATABASE flaskblog;

4. Update database config in app.py

DB_CONFIG = {  
    "host": "localhost",  
    "user": "your_mysql_username",  
    "password": "your_mysql_password",  
    "database": "flaskblog"  
}  

5. Run project

py app.py  

6. Open browser

http://127.0.0.1:5000  

---

## 🔐 Modules

- Authentication Module  
- Post Management (CRUD)  
- Admin Dashboard  
- Navigation System  
- Flash Messages  

---

## 💡 Learning Outcomes

- Flask routing and templates  
- MySQL integration  
- CRUD operations  
- User authentication  
- Bootstrap UI design  
- Git & GitHub usage  

---

## 📸 Screenshots

(Add later)

---

## 👨‍💻 Author

Galla Divya Teja  
GitHub: https://github.com/TejaGalla  

---

## ⭐ Conclusion

This project demonstrates full-stack development using Flask and MySQL with authentication and CRUD functionality.