"""PDF and LaTeX report generation for IndoMarket Insight."""
from pathlib import Path
import math
import pandas as pd
from config import DATA_PROCESSED
from utils import now_stamp, format_idr
from analytics import add_market_features, kpi_summary, correlation_matrix
from quality import data_quality_report


def _safe_text(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "-"
    return str(x).replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")


def _prepare_report_data(df: pd.DataFrame):
    if df is None:
        df = pd.DataFrame()
    work = df.copy()
    if not work.empty and "date" in work.columns:
        work["date"] = pd.to_datetime(work["date"], errors="coerce")
    featured = add_market_features(work) if not work.empty else work
    kpi = kpi_summary(work) if not work.empty else kpi_summary(pd.DataFrame())
    quality = data_quality_report(work)
    latest = pd.DataFrame()
    anomalies = pd.DataFrame()
    if not featured.empty:
        latest = featured.sort_values("date").groupby(["item", "region"], as_index=False).tail(1)
        latest = latest.sort_values("price", ascending=False).head(20)
        anomalies = featured[featured.get("anomaly", False) == True].sort_values("date", ascending=False).head(20)
    return work, featured, kpi, quality, latest, anomalies


def generate_tex_report(df: pd.DataFrame, title="IndoMarket Insight Report", basename="indomarket_report"):
    work, featured, kpi, quality, latest, anomalies = _prepare_report_data(df)
    stamp = now_stamp()
    path = DATA_PROCESSED / f"{stamp}_{basename}.tex"
    latest_rows = ""
    if not latest.empty:
        for _, r in latest.iterrows():
            latest_rows += f"{_safe_text(r.get('date'))} & {_safe_text(r.get('item'))} & {_safe_text(r.get('region'))} & {_safe_text(r.get('category'))} & {_safe_text(format_idr(r.get('price')))} \\\\ \n"
    else:
        latest_rows = "\\multicolumn{5}{l}{No latest data available} \\\\ \n"

    anomaly_rows = ""
    if not anomalies.empty:
        for _, r in anomalies.iterrows():
            z = r.get("zscore_30d")
            z_txt = "-" if pd.isna(z) else f"{z:.2f}"
            anomaly_rows += f"{_safe_text(r.get('date'))} & {_safe_text(r.get('item'))} & {_safe_text(r.get('region'))} & {_safe_text(format_idr(r.get('price')))} & {z_txt} \\\\ \n"
    else:
        anomaly_rows = "\\multicolumn{5}{l}{No anomalies detected} \\\\ \n"

    issues = "\n".join([f"\\item {_safe_text(i)}" for i in quality.get("issues", [])])
    tex = rf"""
\documentclass[11pt,a4paper]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\title{{{_safe_text(title)}}}
\author{{IndoMarket Insight}}
\date{{{stamp}}}
\begin{{document}}
\maketitle

\section*{{Executive Summary}}
\begin{{itemize}}
    \item Rows: {kpi.get('rows', 0):,}
    \item Items: {kpi.get('items', 0)}
    \item Regions: {kpi.get('regions', 0)}
    \item Latest date: {_safe_text(kpi.get('latest_date'))}
    \item Average latest price: {_safe_text(format_idr(kpi.get('avg_price')))}
    \item Detected anomalies: {kpi.get('anomalies', 0)}
    \item Data quality score: {quality.get('score', 0)}/100
\end{{itemize}}

\section*{{Data Quality Notes}}
\begin{{itemize}}
{issues}
\end{{itemize}}

\section*{{Latest Market Values}}
\begin{{longtable}}{{llllr}}
\toprule
Date & Item & Region & Category & Price \\
\midrule
{latest_rows}\bottomrule
\end{{longtable}}

\section*{{Detected Anomalies}}
\begin{{longtable}}{{llllr}}
\toprule
Date & Item & Region & Price & Z-score \\
\midrule
{anomaly_rows}\bottomrule
\end{{longtable}}

\section*{{Methodology}}
The report is generated automatically from the local SQLite observations and processed CSV files. Indicators include moving averages, percentage change, rolling volatility, and z-score based anomaly detection. Google Trends data, if present, is represented as a 0--100 search interest index.

\section*{{Compliance Note}}
Scraping should use official APIs, permitted CSV downloads, or pages allowed by each website's terms and robots.txt policies.

\end{{document}}
"""
    path.write_text(tex, encoding="utf-8")
    return path


def generate_pdf_report(df: pd.DataFrame, title="IndoMarket Insight Report", basename="indomarket_report"):
    """Generate a PDF report using reportlab. Falls back to a text-like PDF layout."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
    except Exception as exc:
        raise ImportError("PDF generation requires reportlab. Run: pip install reportlab") from exc

    work, featured, kpi, quality, latest, anomalies = _prepare_report_data(df)
    stamp = now_stamp()
    path = DATA_PROCESSED / f"{stamp}_{basename}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(title, styles["Title"]))
    story.append(Paragraph(f"Generated: {stamp} | IndoMarket Insight", styles["Normal"]))
    story.append(Spacer(1, 0.4*cm))

    summary_data = [
        ["Metric", "Value"],
        ["Rows", f"{kpi.get('rows', 0):,}"],
        ["Items", str(kpi.get("items", 0))],
        ["Regions", str(kpi.get("regions", 0))],
        ["Latest date", str(kpi.get("latest_date", "-"))],
        ["Average latest price", format_idr(kpi.get("avg_price"))],
        ["Detected anomalies", str(kpi.get("anomalies", 0))],
        ["Data quality score", f"{quality.get('score', 0)}/100"],
    ]
    story.append(Paragraph("Executive Summary", styles["Heading1"]))
    story.append(_make_table(summary_data, colors))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Data Quality Notes", styles["Heading1"]))
    for issue in quality.get("issues", []):
        story.append(Paragraph(f"• {issue}", styles["Normal"]))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Latest Market Values", styles["Heading1"]))
    latest_data = [["Date", "Item", "Region", "Category", "Price"]]
    if latest.empty:
        latest_data.append(["-", "No latest data available", "-", "-", "-"])
    else:
        for _, r in latest.head(20).iterrows():
            latest_data.append([str(r.get("date", "-"))[:10], str(r.get("item", "-"))[:32], str(r.get("region", "-"))[:18], str(r.get("category", "-"))[:18], format_idr(r.get("price"))])
    story.append(_make_table(latest_data, colors))
    story.append(PageBreak())

    # Optional chart page
    chart_path = _make_trend_chart(featured, stamp)
    if chart_path:
        story.append(Paragraph("Trend Chart", styles["Heading1"]))
        try:
            story.append(Image(str(chart_path), width=17*cm, height=8*cm))
            story.append(PageBreak())
        except Exception:
            pass

    story.append(Paragraph("Detected Anomalies", styles["Heading1"]))
    anomaly_data = [["Date", "Item", "Region", "Price", "Z-score"]]
    if anomalies.empty:
        anomaly_data.append(["-", "No anomalies detected", "-", "-", "-"])
    else:
        for _, r in anomalies.head(20).iterrows():
            z = r.get("zscore_30d")
            anomaly_data.append([str(r.get("date", "-"))[:10], str(r.get("item", "-"))[:32], str(r.get("region", "-"))[:18], format_idr(r.get("price")), "-" if pd.isna(z) else f"{z:.2f}"])
    story.append(_make_table(anomaly_data, colors))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Methodology", styles["Heading1"]))
    story.append(Paragraph("This report is generated from SQLite observations and processed CSV files. Indicators include moving averages, percentage change, rolling volatility, z-score anomalies, quality checks, and Google Trends 0-100 search interest when available.", styles["Normal"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Compliance note: scraping should use official APIs, permitted CSV downloads, or pages allowed by each website's terms and robots.txt policies.", styles["Italic"]))

    doc.build(story)
    return path


def _make_table(data, colors):
    from reportlab.platypus import Table, TableStyle
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 10),
    ]))
    return table



def _make_trend_chart(featured, stamp):
    """Create a small PNG chart for PDF embedding. Returns None if matplotlib unavailable."""
    if featured is None or featured.empty:
        return None
    try:
        import matplotlib.pyplot as plt
        from config import DATA_PROCESSED
        tmp = featured.copy()
        tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
        top_items = tmp.groupby("item")["price"].count().sort_values(ascending=False).head(5).index.tolist()
        plot = tmp[tmp["item"].isin(top_items)].groupby(["date", "item"], as_index=False)["price"].mean()
        if plot.empty:
            return None
        fig, ax = plt.subplots(figsize=(10, 4.5))
        for item, g in plot.groupby("item"):
            ax.plot(g["date"], g["price"], label=str(item)[:24], linewidth=1.4)
        ax.set_title("Top item trends")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value / Price")
        ax.grid(True, alpha=.25)
        ax.legend(fontsize=7)
        fig.autofmt_xdate()
        path = DATA_PROCESSED / f"{stamp}_report_trend_chart.png"
        fig.tight_layout()
        fig.savefig(path, dpi=160)
        plt.close(fig)
        return path
    except Exception:
        return None
