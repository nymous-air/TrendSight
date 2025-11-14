from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Configure OpenRouter Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "https://localhost", 
        "X-Title": "Financial Insights Agent"
    }
)

def generate_charts(df):
    """Create and save revenue/expense/profit charts."""
    plt.figure(figsize=(10,5))
    df[["Revenue", "Expenses", "Profit"]].plot()
    plt.title("Financial Trends Over Time")
    plt.xlabel("Entry")
    plt.ylabel("Amount")
    plt.grid(True)

    chart_path = "financial_chart.png"
    plt.savefig(chart_path)
    plt.close()

    print(f"\nChart saved as: {chart_path}")

def analyze_financials(file_path):
    df = pd.read_csv(file_path)

    # Quick summary stats
    summary = df.describe()
    print("\nData Summary:\n", summary)

    # Generate charts
    generate_charts(df)

    # Send financial summary to AI using a FREE model
    response = client.responses.create(
        model="google/gemini-flash-1.5",
        input=[
            {
                "role": "system",
                "content": "You are a professional financial analyst."
            },
            {
                "role": "user",
                "content": f"Analyze these financial statistics and provide a clear insights summary:\n\n{summary.to_string()}"
            }
        ]
    )

    insights = response.output_text
    print("\nAI Insights:\n", insights)

    return insights


# ---------- OPTIONAL: EMAIL NOTIFICATION ----------
def send_email_notification(subject, body, recipient_email):
    import smtplib
    from email.mime.text import MIMEText

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    if not EMAIL_USER or not EMAIL_PASS:
        print("\n⚠️ Email credentials not set. Skipping email.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = recipient_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    print(f"📧 Email sent to {recipient_email}")


# ---------- OPTIONAL: SLACK NOTIFICATION ----------
def send_slack_alert(message):
    import requests

    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not slack_webhook:
        print("\n⚠️ Slack webhook not set. Skipping Slack alert.")
        return

    requests.post(slack_webhook, json={"text": message})
    print("💬 Slack alert sent")


# ---------- MAIN ----------
if __name__ == "__main__":
    insights = analyze_financials("sample_financials.csv")

    # Optional alerting
    send_email_notification(
        subject="Financial Report Ready",
        body=insights,
        recipient_email="example@gmail.com"
    )

    send_slack_alert(f"Financial Analysis Completed:\n{insights}")
