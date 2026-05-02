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

* Pie Chart visualization
* Bar Chart analysis
* Line Chart trends
* Click-based popup charts (Matplotlib)

### 🛠️ Admin Panel

* Admin authentication
* View all users
* Delete users
* View user profiles
* Access user financial statements

---

## 🔐 Admin Credentials

```
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

```
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

* Python 3.11 (Recommended)

---

### 1️⃣ Create Virtual Environment

```
py -3.11 -m venv venv
```

---

### 2️⃣ Activate Virtual Environment

**Windows**

```
venv\Scripts\activate
```

**Mac / Linux**

```
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

If any error occurs:

```
pip install flask bcrypt itsdangerous matplotlib
```

---

### 4️⃣ Run the Application

```
python app.py
```

---

## 🌐 Access the App

```
http://127.0.0.1:5000
```

---

## ⚠️ Important Notes

* Do NOT use quotes (" ") in terminal commands
* Always activate virtual environment before installing packages
* Use Python 3.11 (Python 3.13 may cause issues)
* If charts fail → ensure `matplotlib` is installed

---

## 🛠️ Troubleshooting

### ❌ ModuleNotFoundError

```
pip install flask
```

### ❌ Matplotlib / NumPy Issues

* Recreate virtual environment using Python 3.11

---

## 🔥 Developer Tip

Update dependencies:

```
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

## 👨‍💻 Author

**Pranav Eswar**
**Gopika S S**
**Aju Mathew Thomson**
**Vishnu S**
**San Jobin S**

---
