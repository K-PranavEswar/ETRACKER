```markdown
<div align="center">
  
  # 💰 SmartExpense AI
  
  <p>
    <b>A powerful full-stack expense tracking web application built with Flask.</b>
  </p>

  <img src="[https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)" alt="Python" />
  <img src="[https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)" alt="Flask" />
  <img src="[https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)" alt="SQLite" />
  <img src="[https://img.shields.io/badge/HTML5_&_CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white](https://img.shields.io/badge/HTML5_&_CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)" alt="HTML/CSS" />

  <br />
  <br />

  *[Add a screenshot of your dashboard here]*
</div>

---

## 📖 About The Project

**SmartExpense AI** is designed to help users take control of their finances. Track your daily expenses, monitor your income, and analyze your financial habits through dynamic visualizations. It also includes a robust Admin panel for seamless user management. 

💡 *Built for learning + real-world project experience.*

---

## ✨ Features

### 👤 User Capabilities
- **Authentication**: Secure Registration & Login using Bcrypt encryption.
- **Financial Tracking**: Easy entry and management of Income and Expenses.
- **Analytics Dashboard**: Visual insights using Matplotlib (Pie, Bar, and Line charts).
- **Date Range Filtering**: Filter and view expenses over specific timeframes.
- **Export & Reporting**: View detailed statements and export data as CSV.
- **Budgeting**: Built-in budget calculator.

### 🛠️ Admin Dashboard
- **User Management**: View user profiles, delete users, and monitor activity.
- **System Monitoring**: View all user statements and overarching analytics.

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

> [!WARNING]  
> Make sure you are using **Python 3.11** (Recommended). Using Python 3.13 may cause installation errors with certain dependencies.

### 1️⃣ Clone or Download the Repository
Navigate to your desired folder and open your terminal.

### 2️⃣ Create a Virtual Environment
```bash
py -3.11 -m venv venv

```

### 3️⃣ Activate the Virtual Environment

* **Windows:**
```bash
venv\Scripts\activate

```


* **Mac / Linux:**
```bash
source venv/bin/activate

```



### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt

```

> [!NOTE]
> If installation fails, install the core packages manually:
> `pip install flask bcrypt itsdangerous matplotlib`

### 5️⃣ Run the Application

```bash
python app.py

```

### 6️⃣ Access the App

Open your browser and navigate to:

```text
http://127.0.0.1:5000

```

---

## 🔐 Admin Credentials

To access the admin dashboard, use the following credentials:

| Field | Value |
| --- | --- |
| **Email** | `admin@smartapp.in` |
| **Password** | `admin` |

---

## 📁 Project Structure

```text
ETracker/
│
├── app.py                # Main application file
├── requirements.txt      # Dependency list
├── database.db           # SQLite database
├── templates/            # HTML templates
├── static/               # CSS, JS, and image assets
└── README.md             # Project documentation

```

---

## 🔧 Troubleshooting

| Error | Solution |
| --- | --- |
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install flask` |
| **Matplotlib / NumPy Error** | Ensure you are using Python 3.11. Delete your `venv` folder and recreate it. |
| **Charts not loading** | Verify `matplotlib` is successfully installed and the virtual environment is activated. |

> [!TIP]
> **Developer Tip:** When adding new packages, always update your dependencies file by running:
> `pip freeze > requirements.txt`

---

## 🚀 Future Roadmap

* [ ] Interactive chart animations
* [ ] Advanced AI analytics and spending insights
* [ ] REST API integration
* [ ] Enhanced mobile-responsive UI
* [ ] Dark/Light theme toggle

---
