#  FinCradle — Personal Finance & Expense Tracker

A full-stack personal finance web application built with **Flask** and **MySQL**. FinCradle helps you track income and expenses, manage custom categories, get AI-driven spending insights, and receive credit card cashback recommendations — all behind a secure OTP-verified login system.

---


> Dashboard · AI Advisor · Category Manager

<img width="1899" height="870" alt="image" src="https://github.com/user-attachments/assets/1de8a32a-a159-41eb-8485-421349f4b14f" />


---

##  Features

- **Secure Authentication** — Register with email OTP verification, login with hashed passwords (bcrypt)
- **Income & Expense Tracking** — Log transactions with custom categories and optional notes
- **Custom Categories** — Create and delete your own income/expense categories with weekly/monthly/yearly report toggles
- **Financial Dashboard** — Visual overview of income vs expense with line and pie charts (Chart.js)
- **Savings Summary** — Real-time savings calculation displayed on the dashboard
- **AI Spending Advisor** — Rule-based advisor that detects overspending, identifies spending trends, and recommends the best credit card for cashback
- **Credit Card Recommendations** — Matches your spending categories to card reward rates to suggest the highest-cashback card
- **PDF Report Download** — Export your financial summary as a PDF
- **Responsive UI** — Works on desktop and mobile with a collapsible sidebar

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask |
| Database | MySQL 8.0 via PyMySQL |
| ORM | SQLAlchemy + Flask-SQLAlchemy |
| Auth | Flask-Login, Flask-Bcrypt |
| Email / OTP | Flask-Mail (Gmail SMTP) |
| Frontend | Chart.js, Custom CSS |
| PDF Export | ReportLab |

---

##  Project Structure

```
Expense Tracker/
├── app.py                  # App factory and entry point
├── config.py               # Environment config loader
├── extensions.py           # Flask extensions (db, login, bcrypt, mail)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
│
├── models/
│   ├── user.py             # User model
│   ├── category.py         # Category model
│   ├── income.py           # Income model
│   ├── expense.py          # Expense model
│   ├── credit_card.py      # Credit card model
│   ├── card_reward.py      # Card reward/cashback model
│   └── otp.py
│
├── routes/
│   ├── auth.py             # Register, OTP verify, login, logout
│   ├── finance.py          # Dashboard, add income/expense, categories
│   └── advisor.py          # AI spending advisor
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── verify_otp.html
│   ├── dashboard.html
│   ├── categories.html
│   ├── advisor.html
│   └── report.html
│
├── static/
│   ├── style.css
│   └── main.js
│
└── database.sql            # Full DB schema with all tables and views
```

---

##  Local Setup

### Prerequisites

- Python 3.11 or higher
- MySQL 8.0 + MySQL Workbench
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

---

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set Up the Database

Open **MySQL Workbench**, connect to your local server, then:

1. Go to **File → Open SQL Script**
2. Open `database.sql` from the project folder
3. Click the ⚡ **Execute All** button

This creates the `finance_db` database and all required tables automatically.

---

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_USER=root
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_NAME=finance_db
SECRET_KEY=your_secret_key

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

> **Gmail App Password:** Go to Google Account → Security → 2-Step Verification → App Passwords → generate one for "Mail". Use that as `MAIL_PASSWORD`, not your regular Gmail password.

---

### 6. Update config.py

Open `config.py` and update the database URI with your MySQL password. If your password contains special characters like `@`, use `urllib.parse.quote_plus` to encode it:

```python
from urllib.parse import quote_plus

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
```

---

### 7. Run the Application

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

---

##  Database Schema

| Table | Description |
|---|---|
| `users` | Registered users with hashed passwords |
| `categories` | User-defined income and expense categories |
| `income` | Income transactions linked to categories |
| `expenses` | Expense transactions with optional notes |
| `credit_cards` | Credit card catalog (bank + card name) |
| `card_rewards` | Cashback percentage per card per category |
| `credit_card_benefits` | Detailed benefit rules (caps, frequency) |
| `card_recommendations` | Saved AI recommendations per user |
| `banks` | Bank master list |

A `category_leak_view` SQL view is also created to compare this month vs last month spending per category.

---

##  Authentication Flow

```
Register → OTP sent to email → Verify OTP → Account created → Login
```

OTP is stored in the Flask session and cleared immediately after successful verification. Passwords are hashed with bcrypt before storage.

---

##  AI Advisor Logic

The advisor uses rule-based analysis on your transaction data:

- **Overspending** — Flags if expenses exceed income or cross 70% of income
- **Trend** — Categorises spending as excellent / stable / rising based on expense-to-income ratio
- **Card Recommendation** — Queries `card_rewards` joined with `credit_cards` to find the card with the highest cashback percent and suggests it

---

##  Dependencies

```
Flask
Flask-Login
Flask-SQLAlchemy
Flask-Bcrypt
Flask-CORS
Flask-Mail
python-dotenv
PyMySQL
SQLAlchemy
pandas
numpy
reportlab
requests
beautifulsoup4
jsonschema
```

---

##  Deployment Notes

- Set `debug=False` in `app.py` before deploying to production
- Use environment variables for all secrets — never commit `.env`
- For production, consider switching from Flask's built-in server to **Gunicorn** behind **Nginx**
- Use a managed MySQL instance (e.g. PlanetScale, AWS RDS) instead of localhost

---



---

## 📄 License

This project is for educational and personal use.
