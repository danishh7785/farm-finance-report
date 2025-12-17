from flask import Flask, render_template, request, send_file
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Image,
    Spacer,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
REPORT_DIR = "reports"
STATIC_DIR = "static"
os.makedirs(REPORT_DIR, exist_ok=True)

# ---- COLOR CONSTANTS (CSS-style strings for matplotlib, HexColor for reportlab) ----
PRIMARY_GREEN_HEX = "#16a34a"
ACCENT_GREEN_HEX = "#22c55e"
EXPENSE_RED_HEX = "#ef4444"
EDGE_HEX = "#334155"

PRIMARY_GREEN = colors.HexColor(PRIMARY_GREEN_HEX)
ACCENT_GREEN = colors.HexColor(ACCENT_GREEN_HEX)
DARK_BG = colors.HexColor("#0f172a")
CARD_BG = colors.HexColor("#1e293b")
TEXT_MAIN = colors.HexColor("#e5e7eb")
TEXT_MUTED = colors.HexColor("#9ca3af")
BORDER_SUBTLE = colors.HexColor("#334155")


def footer(canvas, doc):
    """Footer on each page"""
    canvas.saveState()
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.setFillColor(colors.HexColor("#6b7280"))

    # Page number
    page_num = canvas.getPageNumber()
    canvas.drawRightString(7.5 * inch, 0.5 * inch, f"Page {page_num}")

    # Footer branding
    canvas.drawCentredString(
        4.17 * inch,
        0.25 * inch,
        "🌾 Proudly maintained accounting with GramIQ",
    )
    canvas.restoreState()


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/generate", methods=["POST"])
def generate_pdf():
    farmer = request.form["farmer_name"]
    crop = request.form["crop_name"]
    season = request.form["season"]
    acres = float(request.form["acres"])

    # ---- EXPENSES ----
    expenses = []
    total_expense = 0
    for c, a, d, desc in zip(
        request.form.getlist("expense_category[]"),
        request.form.getlist("expense_amount[]"),
        request.form.getlist("expense_date[]"),
        request.form.getlist("expense_desc[]"),
    ):
        if c and a:
            amt = float(a)
            total_expense += amt
            expenses.append([c, f"₹ {amt:,.2f}", d or "—", desc or "—"])

    # ---- INCOME ----
    incomes = []
    total_income = 0
    for c, a, d, desc in zip(
        request.form.getlist("income_category[]"),
        request.form.getlist("income_amount[]"),
        request.form.getlist("income_date[]"),
        request.form.getlist("income_desc[]"),
    ):
        if c and a:
            amt = float(a)
            total_income += amt
            incomes.append([c, f"₹ {amt:,.2f}", d or "—", desc or "—"])

    profit = total_income - total_expense
    cost_per_acre = total_expense / acres if acres > 0 else 0

    # ---- CHART (Matplotlib) ----
    chart_path = os.path.join(STATIC_DIR, "chart.png")
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(6, 3), facecolor="#0f172a")
    ax.set_facecolor("#1e293b")

    bars = ax.bar(
        ["Income", "Expense"],
        [total_income, total_expense],
        color=[ACCENT_GREEN_HEX, EXPENSE_RED_HEX],
        edgecolor=EDGE_HEX,
        linewidth=1.5,
        alpha=0.9,
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"₹{height:,.0f}",
            ha="center",
            va="bottom",
            color="#e5e7eb",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_ylabel("Amount (₹)", color="#9ca3af")
    ax.set_ylim(0, max(total_income, total_expense) * 1.15 if (total_income or total_expense) else 1)
    ax.tick_params(colors="#9ca3af")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(EDGE_HEX)
    ax.spines["bottom"].set_color(EDGE_HEX)

    plt.tight_layout()
    plt.savefig(chart_path, dpi=150, facecolor="#0f172a", edgecolor="none")
    plt.close()

    # ---- PDF SETUP ----
    filename = f"{crop}_{acres}_{season}_{datetime.now().year}.pdf"
    pdf_path = os.path.join(REPORT_DIR, filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        topMargin=0.7 * inch,
        bottomMargin=0.9 * inch,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    section_style = ParagraphStyle(
        "SectionHead",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=ACCENT_GREEN,
        spaceAfter=10,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    metric_style = ParagraphStyle(
        "Metric",
        parent=styles["Normal"],
        fontSize=11,
        textColor=TEXT_MAIN,
        spaceAfter=4,
        fontName="Helvetica",
    )

    info_style = ParagraphStyle(
        "Info",
        parent=styles["Normal"],
        fontSize=10,
        textColor=TEXT_MUTED,
        spaceAfter=2,
        fontName="Helvetica",
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.whitesmoke,
        fontName="Helvetica-Bold",
        alignment=1,
    )

    elements = []

    # ---- HEADER WITH LOGO + INFO ----
    logo_path = os.path.join(STATIC_DIR, "logo.png")
    header_table_data = []

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=0.8 * inch, height=0.8 * inch)
        header_info = [
            Paragraph(f"<b><font size=18 color='{ACCENT_GREEN_HEX}'>{crop}</font></b>", info_style),
            Paragraph(f"<b>Farmer:</b> {farmer}", info_style),
            Paragraph(f"<b>Season:</b> {season} • <b>Area:</b> {acres} acres", info_style),
            Paragraph(
                f"<b>Generated:</b> {datetime.now().strftime('%d %b, %Y at %H:%M')}",
                info_style,
            ),
        ]
        header_table_data = [[logo, header_info]]
        col_widths = [1 * inch, 5.2 * inch]
    else:
        header_info = [
            Paragraph(f"<b><font size=18 color='{ACCENT_GREEN_HEX}'>{crop}</font></b>", info_style),
            Paragraph(f"<b>Farmer:</b> {farmer}", info_style),
            Paragraph(f"<b>Season:</b> {season} • <b>Area:</b> {acres} acres", info_style),
            Paragraph(
                f"<b>Generated:</b> {datetime.now().strftime('%d %b, %Y at %H:%M')}",
                info_style,
            ),
        ]
        header_table_data = [[header_info]]
        col_widths = [6.2 * inch]

    header_table = Table(header_table_data, colWidths=col_widths)
    header_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
                ("BORDER", (0, 0), (-1, -1), 0, colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(header_table)
    elements.append(Spacer(1, 0.2 * inch))

    # ---- SUMMARY METRICS ----
    summary_data = [
        ("Total Income", f"₹ {total_income:,.2f}", ACCENT_GREEN_HEX),
        ("Total Expense", f"₹ {total_expense:,.2f}", EXPENSE_RED_HEX),
        (
            "Profit/Loss",
            f"₹ {profit:,.2f}",
            PRIMARY_GREEN_HEX if profit >= 0 else EXPENSE_RED_HEX,
        ),
    ]

    metric_cells = []
    for label, value, color_hex in summary_data:
        cell_content = [
            Paragraph(f"<font color='#9ca3af' size=9><b>{label}</b></font>", info_style),
            Paragraph(f"<font size=16 color='{color_hex}'><b>{value}</b></font>", metric_style),
        ]
        metric_cells.append(cell_content)

    metric_table = Table([metric_cells], colWidths=[2 * inch, 2 * inch, 2.2 * inch])
    metric_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
                ("BORDER", (0, 0), (-1, -1), 1, BORDER_SUBTLE),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    elements.append(metric_table)
    elements.append(Spacer(1, 0.25 * inch))

    # ---- COST PER ACRE ----
    elements.append(
        Paragraph(f"<b>Cost per Acre:</b> ₹ {cost_per_acre:,.2f}", metric_style)
    )
    elements.append(Spacer(1, 0.15 * inch))

    # ---- CHART ----
    elements.append(Paragraph("<b>Income vs Expense Overview</b>", section_style))
    chart_img = Image(chart_path, width=5.5 * inch, height=2.75 * inch)
    elements.append(chart_img)
    elements.append(Spacer(1, 0.2 * inch))

    # ---- EXPENSE TABLE ----
    elements.append(Paragraph("<b>Expenses Breakdown</b>", section_style))

    expense_headers = [
        Paragraph("<b>Category</b>", table_header_style),
        Paragraph("<b>Amount</b>", table_header_style),
        Paragraph("<b>Date</b>", table_header_style),
        Paragraph("<b>Description</b>", table_header_style),
    ]

    expense_data = (
        [expense_headers] + expenses
        if expenses
        else [expense_headers, ["No expenses recorded", "—", "—", "—"]]
    )

    exp_table = Table(
        expense_data,
        colWidths=[1.5 * inch, 1.2 * inch, 1.3 * inch, 1.2 * inch],
    )
    exp_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), DARK_BG),
                ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_MAIN),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 1, BORDER_SUBTLE),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [DARK_BG, colors.HexColor("#0a0f1a")],
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(exp_table)
    elements.append(Spacer(1, 0.25 * inch))

    # ---- INCOME TABLE ----
    elements.append(Paragraph("<b>Income Breakdown</b>", section_style))

    income_headers = [
        Paragraph("<b>Category</b>", table_header_style),
        Paragraph("<b>Amount</b>", table_header_style),
        Paragraph("<b>Date</b>", table_header_style),
        Paragraph("<b>Description</b>", table_header_style),
    ]

    income_data = (
        [income_headers] + incomes
        if incomes
        else [income_headers, ["No income recorded", "—", "—", "—"]]
    )

    inc_table = Table(
        income_data,
        colWidths=[1.5 * inch, 1.2 * inch, 1.3 * inch, 1.2 * inch],
    )
    inc_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), DARK_BG),
                ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_MAIN),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 1, BORDER_SUBTLE),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [DARK_BG, colors.HexColor("#0a0f1a")],
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(inc_table)

    # ---- BUILD PDF ----
    doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
