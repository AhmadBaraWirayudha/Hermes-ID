"""Webhook and SMTP notification helpers."""
import os
import smtplib
from email.message import EmailMessage
import pandas as pd
import requests
from settings import load_settings


def alerts_to_text(alerts_df: pd.DataFrame, max_rows=20):
    if alerts_df is None or alerts_df.empty:
        return "No alerts."
    lines = ["IndoMarket Insight Alerts", "========================="]
    for _, r in alerts_df.head(max_rows).iterrows():
        lines.append(f"[{r.get('severity','')}] {r.get('type','')}: {r.get('message','')}")
    if len(alerts_df) > max_rows:
        lines.append(f"... and {len(alerts_df)-max_rows} more")
    return "\n".join(lines)


def send_webhook(alerts_df, webhook_url=None):
    settings = load_settings()
    url = webhook_url or settings.get("webhook_url")
    if not url:
        raise ValueError("Webhook URL not configured")
    payload = {"text": alerts_to_text(alerts_df), "alerts": alerts_df.to_dict(orient="records")}
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    return r.status_code


def send_email(alerts_df, smtp_settings=None):
    settings = load_settings()
    smtp = smtp_settings or settings.get("smtp", {})
    if not smtp.get("enabled"):
        raise ValueError("SMTP notifications are disabled")
    password = os.getenv(smtp.get("password_env", "INDOMARKET_SMTP_PASSWORD"), "")
    msg = EmailMessage()
    msg["Subject"] = "IndoMarket Insight Alerts"
    msg["From"] = smtp.get("from_email")
    msg["To"] = smtp.get("to_email")
    msg.set_content(alerts_to_text(alerts_df))
    with smtplib.SMTP(smtp.get("host"), int(smtp.get("port", 587))) as server:
        server.starttls()
        if smtp.get("username"):
            server.login(smtp.get("username"), password)
        server.send_message(msg)
    return True
