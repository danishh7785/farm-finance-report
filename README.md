# Farm Finance PDF Report Generator

Backend Developer Intern – Technical Assignment (GramIQ)

---

## 📌 Project Overview

This project is a backend web application developed as part of the **Backend Developer Intern Technical Assignment**.  
The application collects farm finance data through a simple web-based form and generates a **downloadable PDF report** containing financial summaries, tables, and visualizations.

The system helps farmers or agri-finance teams maintain structured financial records in a clean and readable format.

---

## 🎯 Features

- Web-based form for entering farm finance data
- Support for **multiple expense and income entries**
- Automatic calculation of:
  - Total Income
  - Total Expense
  - Profit or Loss
  - Cost of Cultivation per Acre
- Dynamic PDF report generation
- PDF includes:
  - Company logo
  - Dynamic report title
  - Finance summary
  - Bar chart visualization (Income vs Expense)
  - Expense breakdown table
  - Income breakdown table
  - Auto-generated ledger
  - Footer on every page
- One-click PDF download

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **PDF Generation:** ReportLab  
- **Charts:** Matplotlib  
- **Frontend:** HTML, Bootstrap  
- **Version Control:** Git, GitHub  

---

## 📂 Project Structure

farm-finance-report/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│ ├── logo.png
│ └── chart.png
│
├── templates/
│ └── form.html
│
├── reports/
│ └── (Generated PDFs)



---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/farm-finance-report.git
cd farm-finance-report



2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Application
python app.py

4️⃣ Open in Browser
http://127.0.0.1:5000

🧪 Sample Input (For Demo)

Farmer Name: Ramesh Patil
Crop Name: Wheat
Season: Rabi
Total Acres: 5

Expenses:

Seeds – ₹3500

Fertilizers – ₹4200

Labor – ₹3000

Income:

Sale of Wheat – ₹28000

Government Subsidy – ₹2500

📄 Generated PDF Report Structure

Header

Company logo

Dynamic report title (crop_acres_season_year)

Timestamp

Farmer name

Finance Summary

Total income

Total expense

Profit or loss

Cost of cultivation per acre

Chart

Bar chart showing income vs expense

Expense Breakdown Table

Income Breakdown Table

Ledger

Merged list of all income and expense entries

Footer

“Proudly maintained accounting with GramIQ”

📹 Demo Video

A short demo video (2–4 minutes) demonstrates:

Form input

PDF generation

PDF download and preview

📌 Notes

The application uses ReportLab for PDF generation to ensure compatibility on Windows systems.

Generated PDFs are stored locally and excluded from version control using .gitignore.

✅ Assignment Compliance

This project fulfills all requirements specified in the Backend Developer Intern – Technical Assignment, including:

Backend implementation

Form handling

PDF generation

Chart rendering

Clean layout and structured data

Error-free execution

👤 Author

Danish Gaus
Backend Developer Intern Applicant

📄 License

This project is created for educational and evaluation purposes.


---

## ✅ What to do now

1️⃣ Paste this into `README.md`  
2️⃣ Commit & push:
```bash
git add README.md
git commit -m "Add detailed README"
git push
