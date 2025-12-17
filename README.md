# 🌾 Farm Finance Report Generator

A **Flask-based backend application** that collects farm financial data through a web form and generates a **detailed, professionally formatted PDF farm finance report** using Python.

This project dynamically processes user input, performs financial calculations, generates charts, and creates a multi-section PDF report using **ReportLab and Matplotlib**.

---

## 🎯 Project Objective

The objective of this project is to provide a simple backend system that:

* Accepts structured farm income and expense data
* Calculates financial metrics automatically
* Generates a printable PDF report for record keeping and analysis

This project demonstrates backend development skills, server-side processing, and document generation.

---

## ✨ Core Features

* Flask-based web application
* HTML form for entering farm and crop details
* Supports **multiple income and expense entries**
* Automatic financial calculations:

  * Total income
  * Total expenses
  * Net profit or loss
  * Cost of cultivation per acre
* Dynamic **bar chart generation** (Income vs Expenses)
* Professionally formatted **PDF report**
* Header logo and footer branding
* Timestamped reports
* PDF download on submission

---

## 🧠 How the Application Works

1. User fills out the web form with farm details, income, and expenses
2. Flask processes the form data on submission
3. Financial totals and metrics are calculated server-side
4. A bar chart is generated using Matplotlib
5. A structured PDF is created using ReportLab
6. The PDF is saved locally and returned to the user for download

---

## 🧰 Tech Stack

* **Language:** Python 3
* **Backend Framework:** Flask
* **PDF Generation:** ReportLab (Platypus)
* **Charting:** Matplotlib
* **Frontend:** HTML, Bootstrap
* **Version Control:** Git, GitHub

---

## 📂 Project Structure

```
farm-finance-report/
│
├── app.py                    # Main Flask application logic
├── requirements.txt          # Python dependencies
├── templates/
│   ├── form.html             # Input form UI
│   └── pdf_template.html     # PDF layout reference
├── static/
│   ├── logo.png              # Logo used in PDF header
│   └── chart.png             # Auto-generated chart image
├── reports/                  # Generated PDF reports
├── .gitignore                # Git ignore rules
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/danishh7785/farm-finance-report.git
cd farm-finance-report
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python app.py
```

### 4️⃣ Access the App

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🧪 Input Details

The form accepts:

* Farmer name
* Crop name and season
* Total land area (acres)
* Multiple expense entries (category, amount, date, description)
* Multiple income entries (category, amount, date, description)

---

## 📄 Generated PDF Report Includes

* Report header with logo
* Farmer and crop details
* Date and time of generation
* Financial summary section
* Total income and total expenses
* Net profit or loss
* Cost per acre
* Income vs Expense bar chart
* Expense breakdown table
* Income breakdown table
* Combined financial ledger
* Footer branding text

---

## 📦 Dependencies

Main libraries used in this project:

* Flask
* ReportLab
* Matplotlib

Refer to `requirements.txt` for the complete dependency list.

---

## 📝 Notes

* PDF reports are saved locally inside the `reports/` directory
* Charts are generated dynamically and reused in the PDF
* The project is designed for backend evaluation and demonstration

---

## 👤 Author

**Danish Gaus**
Final-Year Computer Engineering Student

GitHub: [https://github.com/danishh7785](https://github.com/danishh7785)

---

## 📄 License

This project is created for educational and evaluation purposes. You may add an open-source license if required.

---

⭐ Feel free to fork, modify, and enhance this project
