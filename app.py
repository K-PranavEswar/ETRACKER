from flask import Flask, render_template, request, redirect, session, Response
import sqlite3,csv,re
import bcrypt,os
import matplotlib
matplotlib.use('Agg')
import io
from flask import send_file
app = Flask(__name__)
app.secret_key = "secret123"
CSV_FILE = "contact-details.csv"
DB_FILE = "database.db"

# ---------------- DATABASE INIT ----------------
def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                budget REAL DEFAULT 0,
                joined_on TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                title TEXT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                source TEXT,
                amount REAL,
                date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL
            )
        """)

        default_categories = [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment"
        ]

        for category in default_categories:
            try:
                cursor.execute(
                    "INSERT INTO categories (category_name) VALUES (?)",
                    (category,)
                )
            except:
                pass

        try:
            cursor.execute("ALTER TABLE users ADD COLUMN budget REAL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE users ADD COLUMN joined_on TEXT")
        except sqlite3.OperationalError:
            pass

        cursor.execute("""
            UPDATE users
            SET joined_on = date('now')
            WHERE joined_on IS NULL
        """)

        conn.commit()
        conn.close()

    except Exception as e:
        print("DB init error:", e)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/user/<int:user_id>")
def public_user_profile(user_id):
    if "admin" not in session:
        return redirect("/login")

    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fullname, email, joined_on
            FROM users
            WHERE id = ?
        """, (user_id,))
        user = cursor.fetchone()

        conn.close()

        if not user:
            return render_template("error.html", message="User not found")

        return render_template("admin/user_profile.html", user=user)

    except Exception as e:
        return render_template("error.html", message=str(e))

# ---------------- CONTACT ----------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            return render_template("contact.html", error="All fields are required")

        file_exists = os.path.isfile(CSV_FILE)

        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Name", "Email", "Message"])

            writer.writerow([name, email, message])

        return render_template("contact.html", success="Message saved successfully!")

    return render_template("contact.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/reset-password")
def reset_password():
    return render_template("reset-password.html")

@app.route("/send-reset-link", methods=["GET", "POST"])
def send_reset_link():
    try:
        if request.method == "POST":
            email = request.form.get("email")

            if not email:
                return render_template("reset-password.html", error="Email is required")

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

            conn.close()

            if not user:
                return render_template("reset-password.html", error="Email not registered")

            return render_template("reset-password.html", success="Reset link sent successfully!")

        return redirect("/login")

    except:
        return render_template("reset-password.html", error="Something went wrong")

# ---------------- REGISTER ----------------
@app.route("/register-user", methods=["POST"])
def register_user():
    try:
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")

        if not fullname or not email or not password:
            return render_template("register.html", error="All fields are required")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template("register.html", error="Invalid email format")
        
        hashed_password = bcrypt.hashpw(        #bcrypt is a library that provides secure password hashing
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (fullname, email, password, joined_on)
            VALUES (?, ?, ?, date('now'))
            """,
            (fullname, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return render_template(
            "login.html",
            success="Registration successful! Please login."
        )

    except sqlite3.IntegrityError:  # This error occurs when trying to insert a duplicate email due to the UNIQUE constraint
        return render_template("register.html", error="Email already exists")

    except Exception as e:
        return render_template("register.html", error=str(e))

# ---------------- LOGIN ----------------
@app.route("/login-user", methods=["POST"])
def login_user():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template("login.html", error="All fields are required")

        if email == "admin@smartapp.in" and password == "admin":
            session.clear()
            session["admin"] = True
            return redirect("/admin-dashboard")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT fullname, email, password FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            return render_template("login.html", error="Email not found")

        stored_password = user[2]

        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        if not bcrypt.checkpw(password.encode("utf-8"), stored_password):
            return render_template("login.html", error="Wrong password")

        session.clear()
        session["user"] = user[0]
        session["email"] = user[1]

        return redirect("/dashboard")

    except Exception as e:
        return render_template("login.html", error=str(e))
    

@app.route("/fix-db")
def fix_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN joined_on TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        UPDATE users
        SET joined_on = date('now')
        WHERE joined_on IS NULL
    """)

    conn.commit()
    conn.close()

    return "Database fixed successfully"
# ---------------- USER DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Expenses
        cursor.execute(
            "SELECT * FROM expenses WHERE user_email = ?",
            (session["email"],)
        )
        expenses = cursor.fetchall()
        # Total expense
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE user_email = ?",
            (session["email"],)
        )
        total = cursor.fetchone()[0] or 0
        # Monthly
        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE user_email = ?
            AND strftime('%m', date)=strftime('%m','now')
        """, (session["email"],))
        monthly = cursor.fetchone()[0] or 0
        # Income
        cursor.execute(
            "SELECT SUM(amount) FROM income WHERE user_email = ?",
            (session["email"],)
        )
        income = cursor.fetchone()[0] or 0
        balance = income - total
        
        # FETCH CATEGORIES
        cursor.execute("""
            SELECT *
            FROM categories
            ORDER BY category_name ASC
        """)

        categories = cursor.fetchall()

        conn.close()

        return render_template(
            "dashboard.html",
            name=session["user"],
            total=total,
            monthly=monthly,
            expenses=expenses,
            balance=balance,
            income=income,
            categories=categories
        )

    except Exception as e:

        return render_template(
            "error.html",
            message=str(e)
        )
        
# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin-dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/login")

    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(amount),0) FROM expenses")
        total_expenses = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(amount),0) FROM income")
        total_income = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id, fullname, email
            FROM users
            ORDER BY id DESC
            LIMIT 5
        """)
        active_users = [
            {"id": row["id"], "username": row["fullname"]}
            for row in cursor.fetchall()
        ]

        active_users_count = len(active_users)

        cursor.execute("""
            SELECT u.fullname, e.title, e.amount, e.category, e.date
            FROM expenses e
            JOIN users u ON e.user_email = u.email
            ORDER BY e.id DESC
            LIMIT 8
        """)
        recent_activities = cursor.fetchall()

        cursor.execute("""
            SELECT date, SUM(amount) as total
            FROM expenses
            GROUP BY date
            ORDER BY date DESC
            LIMIT 7
        """)
        recent_trend = cursor.fetchall()

        trend_labels = [row["date"] for row in reversed(recent_trend)]     #x axis labels (dates)
        trend_values = [row["total"] for row in reversed(recent_trend)]    #y axis values (total expenses)

        conn.close()

        return render_template(
            "admin/admin.html",
            total_expenses=round(total_expenses, 2),
            total_income=round(total_income, 2),
            total_users=total_users,
            active_users_count=active_users_count,
            active_users=active_users,
            recent_activities=recent_activities,
            trend_labels=trend_labels,
            trend_values=trend_values
        )

    except Exception as e:
        return render_template("error.html", message=f"Admin error: {str(e)}")

# ---------------- ADMIN CATEGORY MANAGEMENT ----------------
@app.route("/admin/category", methods=["GET", "POST"])
def admin_category():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    if request.method == "POST":

        category = request.form.get("category")

        if category:

            try:

                cursor.execute(
                    "INSERT INTO categories(category_name) VALUES(?)",
                    (category,)
                )

                conn.commit()

            except:
                pass

        return redirect("/admin/category")

    cursor.execute("""
        SELECT * FROM categories
        ORDER BY category_name ASC
    """)

    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "admin/category.html",
        categories=categories
    )
@app.route("/delete-category/<int:id>")
def delete_category(id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM categories WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin/category")

#------------------ USER PROFILE in admin ----------------

@app.route("/admin/user/<int:user_id>")
def user_profile(user_id):
    if "admin" not in session:
        return redirect("/login")

    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fullname, email, joined_on
            FROM users
            WHERE id = ?
        """, (user_id,))
        user = cursor.fetchone()

        conn.close()

        if not user:
            return render_template("error.html", message="User not found")

        return render_template("admin/user_profile.html", user=user)

    except Exception as e:
        return render_template("error.html", message=str(e))

@app.route("/admin/users")
def admin_users():
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fullname, email, joined_on
        FROM users
        ORDER BY id DESC
    """)
    db_users = cursor.fetchall()

    users = []

    for u in db_users:
        user_id = u["id"]
        fullname = u["fullname"]
        email = u["email"]
        joined_on = u["joined_on"] or "N/A"

        cursor.execute(
            "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_email=?",
            (email,)
        )
        total_expense = cursor.fetchone()[0]

        cursor.execute(
        "SELECT COALESCE(SUM(amount),0) FROM income WHERE user_email=?", (email,)
        )
        total_income = cursor.fetchone()[0]

        users.append({
            "id": user_id,
            "username": fullname,
            "email": email,
            "joined_on": joined_on,
            "total_expense": total_expense,
            "total_income": total_income
        })

    conn.close()
    return render_template("admin/users.html", users=users)

@app.route("/admin/user-expense-chart/<int:user_id>")
def user_expense_chart(user_id):
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        return "No user"

    email = user[0]

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_email=?
        GROUP BY category
    """, (email,))

    data = cursor.fetchall()
    conn.close()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    import matplotlib.pyplot as plt
    import io
    from flask import send_file

    plt.style.use('dark_background')
    plt.figure(figsize=(5,4), facecolor='none')

    colors = [
    '#e6af2e',  # gold
    '#1abc9c',  # teal
    '#e74c3c',  # red
    '#3498db',  # blue
    '#9b59b6'   # purple
    ]

    plt.pie(
    amounts,
    labels=categories,
    autopct='%1.1f%%',
    colors=colors[:len(categories)],
    textprops={'color': '#ffffff', 'fontsize': 10},
    wedgeprops={'linewidth': 2, 'edgecolor': '#0d1210'}
    )

    img = io.BytesIO()
    plt.savefig(img, format='png', transparent=True, bbox_inches='tight')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


@app.route("/admin/settings")
def admin_settings():
    if "admin" not in session:
        return redirect("/login")

    theme = session.get("admin_theme", "dark")

    return render_template(
        "admin/ad-settings.html",
        theme=theme
    )


@app.route("/admin/settings/save", methods=["POST"])
def save_admin_settings():
    if "admin" not in session:
        return redirect("/login")

    theme = request.form.get("theme", "dark")

    session["admin_theme"] = theme

    return redirect("/admin-dashboard")

@app.route("/admin/user-expense-analytics/<int:user_id>")
def user_expense_analytics(user_id):
    if "admin" not in session:
        return {"error": "Unauthorized"}, 401

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return {"error": "User not found"}, 404

        email = user[0]

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_email = ?
            GROUP BY category
        """, (email,))
        pie = cursor.fetchall()

        cursor.execute("""
            SELECT date, SUM(amount)
            FROM expenses
            WHERE user_email = ?
            GROUP BY date
            ORDER BY date ASC
        """, (email,))
        trend = cursor.fetchall()

        conn.close()

        return {
            "pie_labels": [row[0] for row in pie],
            "pie_values": [row[1] for row in pie],
            "trend_labels": [row[0] for row in trend],
            "trend_values": [row[1] for row in trend]
        }

    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    if "admin" not in session:
        return redirect("/login")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Step 1: Get user email
        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return "User not found"

        email = user[0]

        # Step 2: Delete related data first
        cursor.execute("DELETE FROM expenses WHERE user_email = ?", (email,))
        cursor.execute("DELETE FROM income WHERE user_email = ?", (email,))

        # Step 3: Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

        conn.commit()
        conn.close()

        return redirect("/admin/users")

    except Exception as e:
        return str(e)

#----------------- BUDGET CALCULATOR ----------------
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. If user submits the form, save it to the DB
    if request.method == 'POST':
        new_budget = float(request.form['budget'])
        cursor.execute("UPDATE users SET budget = ? WHERE email = ?", (new_budget, session["email"]))
        conn.commit()

    # 2. Fetch the user's saved budget
    cursor.execute("SELECT budget FROM users WHERE email = ?", (session["email"],))
    user_budget = cursor.fetchone()[0] or 0

    # 3. Calculate actual total spent THIS MONTH from the expenses table
    cursor.execute("""
        SELECT SUM(amount) FROM expenses 
        WHERE user_email = ? AND strftime('%m', date) = strftime('%m', 'now')
    """, (session["email"],))
    spent = cursor.fetchone()[0] or 0

    conn.close()

    budget_val = user_budget
    message = ""

    if budget_val > 0:
        percent = int((spent / budget_val) * 100)
        remaining = budget_val - spent
        if percent > 80:
            message = "Warning: You are close to your limit!"
        else:
            message = "You're managing your budget well 👍"
    else:
        percent = 0
        remaining = 0

    return render_template("budget.html",
        budget=budget_val, spent=spent, remaining=remaining,
        percent=percent, message=message
    )

# ---------------- SETTINGS ----------------
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if "user" not in session:
        return redirect("/login")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    success_budget = False
    success_income = False

    if request.method == 'POST':

        # ✅ Budget update
        if 'budget' in request.form:
            new_budget = float(request.form.get('budget', 0))
            cursor.execute(
                "UPDATE users SET budget = ? WHERE email = ?",
                (new_budget, session["email"])
            )
            conn.commit()
            success_budget = True

        # ✅ Income update (bank balance)
        if 'income' in request.form:
            amount = float(request.form.get('income', 0))

            if amount > 0:
                cursor.execute(
                    "INSERT INTO income (user_email, source, amount, date) VALUES (?, ?, ?, date('now'))",
                    (session["email"], "Manual Add", amount)
                )
                conn.commit()
                success_income = True

    # Fetch current budget
    cursor.execute("SELECT budget FROM users WHERE email = ?", (session["email"],))
    current_budget = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        "settings.html",
        current_budget=current_budget,
        success_budget=success_budget,
        success_income=success_income,
        password_success=False,
        password_error=None
    )

@app.route('/reset-data', methods=['POST'])
def reset_data():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Delete all user expenses
        cursor.execute("DELETE FROM expenses WHERE user_email = ?", (session["email"],))

        # Delete all user income
        cursor.execute("DELETE FROM income WHERE user_email = ?", (session["email"],))

        # Reset budget to 0
        cursor.execute("UPDATE users SET budget = 0 WHERE email = ?", (session["email"],))

        conn.commit()
        conn.close()

        return render_template("settings.html", reset_success=True)

    except Exception as e:
        conn.close()
        return render_template("settings.html", reset_error=str(e))
    
@app.route('/change-password', methods=['POST'])
def change_password():
    if "user" not in session:
        return redirect("/login")

    current = request.form.get("current_password")
    new = request.form.get("new_password")
    confirm = request.form.get("confirm_password")

    if new != confirm:
        return render_template("settings.html", password_error="Passwords do not match")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email=?", (session["email"],))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return render_template("settings.html", password_error="User not found")

    stored_password = user[0]

    if isinstance(stored_password, str):
        stored_password = stored_password.encode("utf-8")

    if not bcrypt.checkpw(current.encode("utf-8"), stored_password):
        conn.close()
        return render_template("settings.html", password_error="Current password is incorrect")

    new_hashed = bcrypt.hashpw(new.encode("utf-8"), bcrypt.gensalt())

    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (new_hashed, session["email"])
    )

    conn.commit()
    conn.close()

    return render_template("settings.html", password_success=True)

# ---------------- ADD EXPENSE ----------------
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # Fetch categories
    cursor.execute("""
        SELECT * FROM categories
        ORDER BY category_name ASC
    """)

    categories = cursor.fetchall()

    # ---------------- POST ----------------

    if request.method == "POST":

        try:

            title = request.form.get("title")
            amount = request.form.get("amount")
            category = request.form.get("category")
            date = request.form.get("date")

            if not title or not amount or not category or not date:

                return render_template(
                    "add_expense.html",
                    error="All fields required",
                    categories=categories
                )

            cursor.execute(
                """
                INSERT INTO expenses
                (user_email, title, amount, category, date)

                VALUES (?, ?, ?, ?, ?)
                """,

                (
                    session["email"],
                    title,
                    amount,
                    category,
                    date
                )
            )

            conn.commit()

            return redirect("/dashboard")

        except Exception as e:

            return render_template(
                "add_expense.html",
                error=str(e),
                categories=categories
            )

    # ---------------- GET ----------------

    return render_template(
        "add_expense.html",
        categories=categories
    )
# ---------------- ANALYTICS ----------------
@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")

    return render_template("analytics.html")

def get_filtered_query(base_query):
    from flask import request

    from_date = request.args.get("from")
    to_date = request.args.get("to")

    query = base_query + " WHERE user_email = ?"
    params = [session["email"]]

    if from_date and to_date:
        query += " AND date BETWEEN ? AND ?"
        params.extend([from_date, to_date])

    return query, params

# ---------------- PIE CHART ----------------    
@app.route("/chart/pie")
def chart_pie():
    if "user" not in session:
        return redirect("/login")

    try:
        base_query = """
            SELECT category, SUM(amount)
            FROM expenses
        """

        query, params = get_filtered_query(base_query)
        query += " GROUP BY category"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        if not data:
            categories = ["No Data"]
            amounts = [1]
        else:
            categories = [str(row[0]) for row in data]
            amounts = [float(row[1]) for row in data]

        import matplotlib.pyplot as plt

        plt.close('all')
        plt.figure(figsize=(6,6), facecolor='none')

        colors = ['#e6af2e', '#2ecc71', '#3498db', '#9b59b6']

        plt.pie(
             amounts,
             labels=categories,
             autopct='%1.1f%%',
             colors=colors[:len(categories)],
             textprops={'color': '#ffffff'}
        )

        img = io.BytesIO()
        plt.savefig(img, format='png', transparent=True, bbox_inches='tight')
        img.seek(0)
        plt.close()
        return send_file(img, mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- BAR CHART ----------------
@app.route("/chart/bar")
def chart_bar():
    if "user" not in session:
        return redirect("/login")

    try:
        base_query = """
            SELECT category, SUM(amount)
            FROM expenses
        """

        query, params = get_filtered_query(base_query)
        query += " GROUP BY category"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        # ✅ Handle empty data
        if not data:
            categories = ["No Data"]
            values = [0]
        else:
            categories = [row[0] for row in data]
            values = [float(row[1]) for row in data]

        import matplotlib.pyplot as plt

        plt.close('all')
        plt.figure(figsize=(6,4), facecolor='none')

        colors = ['#e6af2e', '#2ecc71', '#3498db', '#9b59b6']

        bars = plt.bar(
            categories,
            values,
            color=colors[:len(categories)]
        )

        # ✅ Label settings
        plt.xlabel("Category", color='white')
        plt.ylabel("Amount", color='white')
        plt.xticks(rotation=20, color='white')
        plt.yticks(color='white')

        # ✅ Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                color='white',
                fontsize=9
            )

        img = io.BytesIO()
        plt.savefig(
            img,
            format='png',
            transparent=True,
            bbox_inches='tight'
        )
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- LINE CHART ----------------
@app.route("/chart/line")
def chart_line():
    if "user" not in session:
        return redirect("/login")

    try:
        base_query = """
            SELECT date, SUM(amount)
            FROM expenses
        """

        query, params = get_filtered_query(base_query)
        query += " GROUP BY date ORDER BY date ASC"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        # ✅ Handle empty data
        if not data:
            dates = ["No Data"]
            values = [0]
        else:
            dates = [row[0] for row in data]
            values = [float(row[1]) for row in data]

        import matplotlib.pyplot as plt

        plt.close('all')
        plt.figure(figsize=(6,4), facecolor='none')

        plt.plot(
            dates,
            values,
            marker='o',
            color='#e6af2e',
            linewidth=2
        )

        # ✅ Axis styling
        plt.xlabel("Date", color='white')
        plt.ylabel("Amount", color='white')
        plt.xticks(rotation=30, color='white')
        plt.yticks(color='white')

        # ✅ Value labels
        for i, v in enumerate(values):
            plt.text(
                dates[i],
                v,
                str(int(v)),
                ha='center',
                va='bottom',
                color='white',
                fontsize=8
            )

        img = io.BytesIO()
        plt.savefig(
            img,
            format='png',
            transparent=True,
            bbox_inches='tight'
        )
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}"
# ---------------- ERROR HANDLERS ----------------

@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

# ---------------- STATEMENT ----------------
@app.route("/statement")
def statement():
    if "user" not in session:
        return redirect("/login")

    search_query = request.args.get('search')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT title, amount, category, date FROM expenses WHERE user_email = ?"
    params = [session["email"]]

    if search_query:
        query += " AND (title LIKE ? OR category LIKE ?)"
        search_term = f"%{search_query}%"
        params.extend([search_term, search_term])

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC"

    cursor.execute(query, tuple(params))
    expenses = cursor.fetchall()

    # ✅ TOTAL EXPENSE CALCULATION
    total_expense = sum([exp[1] for exp in expenses]) if expenses else 0

    conn.close()

    return render_template(
        "statement.html",
        expenses=expenses,
        total_expense=total_expense
    )

# ---------------- EXPORT CSV ----------------
@app.route("/export-csv")
def export_csv():
    if "user" not in session:
        return redirect("/login")

    search_query = request.args.get('search')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT title, amount, category, date FROM expenses WHERE user_email = ?"
    params = [session["email"]]

    if search_query:
        query += " AND (title LIKE ? OR category LIKE ?)"
        search_term = f"%{search_query}%"
        params.extend([search_term, search_term])

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC"

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    conn.close()

    def generate():
        yield "Title,Amount,Category,Date\n"
        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]}\n"

    return Response(
        generate(), 
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=SmartExpense_Statement.csv"}
    )

@app.route('/update-currency', methods=['POST'])
def update_currency():
    # This catches the dropdown value from settings.html
    selected_currency = request.form.get('currency')
    
    # Save it to the user's session so the dashboard can read it
    session['currency'] = selected_currency
    
    # Send the user back to the settings page automatically
    return redirect('/settings')

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- GLOBAL ERROR ----------------
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Server error"), 500

# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))