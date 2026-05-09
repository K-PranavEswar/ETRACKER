# 💰 SmartExpense AI

A full-stack expense tracking web application built using Flask.
Manage expenses, track income, analyze financial habits, and monitor users through an admin dashboard.

---

## 🔐 Admin Login

```
Email    : admin@smartapp.in  
Password : admin
```

---

## 🚀 Setup Instructions

### ⚠️ Prerequisite

Make sure you are using:

```
Python 3.11 (Recommended)
```

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

If installation fails, install manually:

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

## ✨ Features

* 👤 User Registration & Login (Bcrypt encryption)
* 💸 Expense Tracking
* 💰 Income Management
* 📊 Analytics Dashboard

  * Pie Chart
  * Bar Chart
  * Line Chart
* 📅 Date Range Filtering
* 🧾 Statement View & CSV Export
* 📉 Budget Calculator
* 🛠️ Admin Dashboard
* 👥 User Management

  * View Profile
  * Delete User
  * View Statement
* 📊 Click-based Popup Chart (Matplotlib)

---

## 📦 Tech Stack

* **Backend**: Flask (Python)
* **Database**: SQLite
* **Charts**: Matplotlib
* **Authentication**: Bcrypt
* **Frontend**: HTML, CSS, JavaScript

---

## 📁 Project Structure

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

## ⚠️ Important Notes

* Do **not use quotes (" ")** while running commands
* Always activate virtual environment before installing packages
* Use **Python 3.11** (Python 3.13 may cause installation errors)
* If charts don’t load → ensure `matplotlib` is installed

---

## 🔧 Troubleshooting

### ❌ ModuleNotFoundError

```
pip install flask
```

### ❌ Matplotlib / NumPy Error

➡️ Use Python 3.11 and recreate virtual environment

---

## 🔥 Developer Tip

Update dependencies:

```
pip freeze > requirements.txt
```

---

## 🚀 Future Improvements

* Chart animations
* Advanced analytics insights
* REST API integration
* Mobile responsive UI
* Dark/Light theme toggle

---

### 💡 Built for learning + real-world project experience


#monthly , #income , #balance , #total ,#expenses = variables