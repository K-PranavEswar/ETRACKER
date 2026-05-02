# 💰 SmartExpense AI

A full-stack **expense tracking web application** built with Flask to help users manage finances efficiently.
Track income, monitor expenses, analyze spending habits, and manage users through a powerful admin dashboard.

---

## 🚀 Features

### 👤 User Module

* Secure Registration & Login (Bcrypt encryption)
* Add, edit, and delete expenses
* Income tracking system
* Date-wise filtering
* Statement view with CSV export
* Budget calculator

### 📊 Analytics

* Pie chart visualization
* Bar chart analysis
* Line chart trends
* Click-based popup charts (Matplotlib)

### 🛠️ Admin Panel

* Admin authentication
* View all users
* Delete users
* View user profiles
* Access user financial statements

---

## 🔐 Admin Credentials

```bash
Email    : admin@smartapp.in
Password : admin
```

---

## 🧰 Tech Stack

| Layer    | Technology            |
| -------- | --------------------- |
| Backend  | Flask (Python)        |
| Database | SQLite                |
| Charts   | Matplotlib            |
| Auth     | Bcrypt                |
| Frontend | HTML, CSS, JavaScript |

---

## 📦 Project Structure

```bash
ETracker/
│
├── app.py
├── requirements.txt
├── database.db
├── templates/
├── static/
└── README.md
```

---

## ⚙️ Installation & Setup

### 🔹 Prerequisites

```bash
Python 3.11
```

---

### 1️⃣ Create Virtual Environment

```bash
py -3.11 -m venv venv
```

---

### 2️⃣ Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If installation fails:

```bash
pip install flask bcrypt itsdangerous matplotlib
```

---

### 4️⃣ Run the Application

```bash
python app.py
```

---

## 🌐 Access the App

```bash
http://127.0.0.1:5000
```

---

## ⚠️ Important Notes

* Do **NOT** use quotes (" ") in terminal commands
* Always activate virtual environment before installing packages
* Use **Python 3.11** (Python 3.13 may cause compatibility issues)
* If charts don’t load → ensure `matplotlib` is installed

---

## 🛠️ Troubleshooting

### ❌ ModuleNotFoundError

```bash
pip install flask
```

### ❌ Matplotlib / NumPy Issues

```bash
# Recreate virtual environment using Python 3.11
```

---

## 🔥 Developer Tip

```bash
pip freeze > requirements.txt
```

---

## 🚀 Future Enhancements

* Dark / Light mode toggle
* Mobile responsive UI
* REST API integration
* Advanced analytics insights
* Animated charts

---

## 📌 Purpose

This project is designed for:

* Learning full-stack development
* Understanding real-world expense management systems
* Practicing Flask + data visualization

---

## 👨‍💻 Authors

* **Pranav Eswar**
* **Gopika S S**
* **Aju Mathew Thomson**
* **Vishnu S**
* **San Jobin S**

