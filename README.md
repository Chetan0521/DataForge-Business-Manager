# 🚀 DataForge – Smart Business Data Manager

DataForge is a full-stack web application built using Flask and MySQL to manage business operations like customers, products, and orders with real-time analytics.

---

## 🧠 Project Overview

This project simulates a real-world business system where users can:
- Manage customers
- Manage products & inventory
- Create and track orders
- View business analytics (revenue, counts)

---

## ⚙️ Tech Stack

- Backend: Python (Flask)
- Database: MySQL
- Frontend: HTML, CSS (Custom UI)
- Connector: mysql-connector-python

---

## 🔥 Features

### 🔐 Authentication
- Login system using MySQL
- Session management

### 👤 Customer Management
- Add customers
- View customer list

### 📦 Product Management
- Add products
- Manage stock

### 🛒 Order System
- Create orders
- Auto price calculation
- Stock update after order

### 📊 Dashboard Analytics
- Total Customers
- Total Products
- Total Orders
- Total Revenue

---

## 🗄️ Database Design

Tables used:
- users
- customers
- products
- orders
- order_items

Relational mapping:
- One customer → Many orders
- One order → Many products

---

## 🏗️ Project Structure


DataForge-Business-Manager/
│── app.py
│── database.sql
│── requirements.txt
│── README.md
│
├── templates/
│ ├── login.html
│ ├── dashboard.html
│ ├── customers.html
│ ├── products.html
│ ├── orders.html
│
├── static/
│ ├── style.css



---

## ▶️ How to Run
### 1. Clone Repository

git clone https://github.com/YOUR_USERNAME/DataForge-Business-Manager.git

cd DataForge-Business-Manager


### 2. Create Virtual Environment

python -m venv .venv
..venv\Scripts\activate


### 3. Install Dependencies
pip install -r requirements.txt



### 4. Setup MySQL
- Create database:

CREATE DATABASE dataforge;

- Run:
mysql -u root -p dataforge < database.sql


### 5. Run App
python app.py


Open browser:
http://127.0.0.1:5000/



---

## 🔑 Default Login

- Username: admin  
- Password: admin123  

---

## 📈 Future Enhancements

- Edit & Delete functionality
- Data visualization (charts)
- Export reports (CSV)
- Secure password hashing
- Deployment (Render / Railway)

---

## 💡 Author

Chetan Shinde  
Aspiring Data Scientist | Python Developer  

---

## ⭐ If you like this project
Give it a star on GitHub ⭐